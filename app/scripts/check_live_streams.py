"""Check whether each stream-bar URL is currently live.

Twitch uses the Helix API (same keys as get_twitch_images.py).
YouTube checks the channel's /live page.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Iterable
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

# How long every visitor can share one answer. Matches the stream bar poll.
_CACHE_SECONDS = 60
_cache_at = 0.0
_cache_key: tuple[str, ...] = ()
_cache_live: list[str] = []
# Only one Twitch / YouTube check runs at a time. Others wait for that answer.
_refresh_lock = threading.Lock()

_twitch_token = ""
_twitch_token_exp = 0.0

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _channel_from_url(href: str) -> str:
    """Pull the channel name from a Twitch or YouTube URL."""
    path = urlparse(href).path.strip("/")
    if not path:
        return ""
    return path.split("/")[0]


def _twitch_access_token() -> str:
    """Ask Twitch for an app token, and keep it until it is close to expiring."""
    global _twitch_token, _twitch_token_exp

    now = time.time()
    if _twitch_token and now < _twitch_token_exp:
        return _twitch_token

    client_id = os.getenv("TWITCH_PUBLIC_KEY", "")
    client_secret = os.getenv("TWITCH_PRIVATE_KEY", "")
    if not client_id or not client_secret:
        return ""

    try:
        auth_resp = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            timeout=10,
        )
        payload = auth_resp.json()
    except (requests.RequestException, ValueError):
        return ""

    token = payload.get("access_token", "")
    if not token:
        return ""

    # Refresh a minute early so we never send an expired token.
    expires_in = int(payload.get("expires_in", 3600))
    _twitch_token = token
    _twitch_token_exp = now + max(expires_in - 60, 30)
    return _twitch_token


def _twitch_live_logins(logins: list[str]) -> set[str]:
    """Return the login names that are on air right now."""
    if not logins:
        return set()

    client_id = os.getenv("TWITCH_PUBLIC_KEY", "")
    token = _twitch_access_token()
    if not client_id or not token:
        return _twitch_live_logins_from_html(logins)

    try:
        resp = requests.get(
            "https://api.twitch.tv/helix/streams",
            params=[("user_login", login) for login in logins],
            headers={
                "Client-ID": client_id,
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return _twitch_live_logins_from_html(logins)
        data = resp.json().get("data", [])
    except (requests.RequestException, ValueError, AttributeError):
        return _twitch_live_logins_from_html(logins)

    return {str(stream.get("user_login", "")).lower() for stream in data if stream}


def _twitch_live_logins_from_html(logins: list[str]) -> set[str]:
    """Fallback: Twitch channel pages mark a live broadcast in their HTML."""
    live: set[str] = set()
    for login in logins:
        try:
            resp = requests.get(
                f"https://www.twitch.tv/{login}",
                headers=_HEADERS,
                timeout=10,
            )
        except requests.RequestException:
            continue
        page = resp.text
        if '"isLiveBroadcast":true' in page or '"isLiveBroadcast": true' in page:
            live.add(login.lower())
    return live


def _youtube_is_live(href: str) -> bool:
    """True when the YouTube channel URL is broadcasting right now."""
    live_url = href.rstrip("/") + "/live"
    try:
        resp = requests.get(
            live_url,
            headers=_HEADERS,
            timeout=10,
            allow_redirects=True,
        )
    except requests.RequestException:
        return False

    # A live channel sends you to a /watch?v= video.
    if "watch?v=" in resp.url:
        return True

    page = resp.text
    return '"isLiveNow":true' in page or '"isLive":true' in page


def _link_key(links: Iterable[dict]) -> tuple[str, ...]:
    """The stream URLs, in order, so we know when the card list changed."""
    return tuple(str(link.get("href", "")) for link in links)


def _cache_is_fresh(key: tuple[str, ...]) -> bool:
    """True when the saved answer is for these URLs and is still new enough."""
    return bool(_cache_at) and key == _cache_key and (time.time() - _cache_at) < _CACHE_SECONDS


def _query_live_hrefs(snapshot: list[dict]) -> list[str]:
    """Ask Twitch and YouTube which of these cards are on air right now."""
    twitch_links = [
        link
        for link in snapshot
        if link.get("platform") == "twitch" and link.get("href")
    ]
    youtube_links = [
        link
        for link in snapshot
        if link.get("platform") == "youtube" and link.get("href")
    ]

    twitch_by_login: dict[str, str] = {}
    for link in twitch_links:
        login = _channel_from_url(str(link["href"])).lower()
        if login:
            twitch_by_login[login] = str(link["href"])

    live_logins = _twitch_live_logins(list(twitch_by_login))
    live_hrefs = [twitch_by_login[login] for login in live_logins if login in twitch_by_login]

    for link in youtube_links:
        href = str(link["href"])
        if _youtube_is_live(href):
            live_hrefs.append(href)

    # Keep caller order, not the API's order.
    href_set = set(live_hrefs)
    return [str(link["href"]) for link in snapshot if link.get("href") in href_set]


def _store_cache(key: tuple[str, ...], ordered: list[str]) -> list[str]:
    """Remember this answer so the next visitor can reuse it."""
    global _cache_at, _cache_key, _cache_live

    _cache_at = time.time()
    _cache_key = key
    _cache_live = ordered
    return list(ordered)


def refresh_live_cache(links: Iterable[dict]) -> list[str]:
    """Ask the APIs again and replace the shared answer.

    The server loop calls this about once a minute. If a check is already
    running, this waits for that answer instead of starting a second one.
    """
    snapshot = list(links)
    key = _link_key(snapshot)
    with _refresh_lock:
        # A visitor's check may have finished while we waited for the lock.
        if _cache_is_fresh(key):
            return list(_cache_live)
        return _store_cache(key, _query_live_hrefs(snapshot))


def fetch_live_hrefs(links: Iterable[dict]) -> list[str]:
    """Return the href of every stream card that is currently live.

    Visitors share one recent answer. A new check starts only when that
    answer is missing or older than `_CACHE_SECONDS`.
    """
    snapshot = list(links)
    key = _link_key(snapshot)
    if _cache_is_fresh(key):
        return list(_cache_live)

    with _refresh_lock:
        # Another visitor may have finished the check while we waited.
        if _cache_is_fresh(key):
            return list(_cache_live)
        return _store_cache(key, _query_live_hrefs(snapshot))


if __name__ == "__main__":
    from app.states.stream_state import STREAM_LINKS

    print(fetch_live_hrefs(STREAM_LINKS))
