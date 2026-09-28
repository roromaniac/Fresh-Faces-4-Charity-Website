from typing import TypedDict

import asyncio

import reflex as rx

from app.scripts.check_live_streams import fetch_live_hrefs


class StreamLink(TypedDict):
    label: str
    caption: str
    href: str
    platform: str
    icon: str
    wordmark: str
    is_live: bool


# Plain Python list so the live-check script can read the URLs without Reflex Vars.
STREAM_LINKS: list[StreamLink] = [
    {
        "label": "Fresh Faces",
        "caption": "Main Tournament",
        "href": "https://www.twitch.tv/roromaniac8",
        "platform": "twitch",
        "icon": "twitch",
        "wordmark": "Twitch",
        "is_live": False,
    },
    {
        "label": "Graduated Faces",
        "caption": "Alumni Stage",
        "href": "https://www.twitch.tv/WallpeSH",
        "platform": "twitch",
        "icon": "twitch",
        "wordmark": "Twitch",
        "is_live": False,
    },
    {
        "label": "Veterans Division",
        "caption": "Masters Arena",
        "href": "https://www.twitch.tv/KH2FMRando",
        "platform": "twitch",
        "icon": "twitch",
        "wordmark": "Twitch",
        "is_live": False,
    },
    {
        "label": "Full Matches",
        "caption": "Archive VODs",
        "href": "https://www.youtube.com/@roroKH2FMR",
        "platform": "youtube",
        "icon": "youtube",
        "wordmark": "YouTube",
        "is_live": False,
    },
]


class StreamState(rx.State):
    """Configurable stream / archive portal links.

    Swap the `href` values for the real Twitch and YouTube URLs when they are
    finalized. Safe, non-broken placeholders are used until then.
    """

    # How often each browser copies the shared live/offline answer.
    poll_ms: int = 60000

    links: list[StreamLink] = STREAM_LINKS

    @rx.var
    def rest_links(self) -> list[StreamLink]:
        # Cards that are not live stay in their original order on the right.
        return [link for link in self.links if not link["is_live"]]

    @rx.var
    def live_links(self) -> list[StreamLink]:
        # Live cards keep that same rest order, grouped on the left.
        return [link for link in self.links if link["is_live"]]

    @rx.var
    def bar_links(self) -> list[StreamLink]:
        # One list so the mobile grid can pack two cards per row.
        live = [link for link in self.links if link["is_live"]]
        rest = [link for link in self.links if not link["is_live"]]
        return live + rest

    @rx.event(background=True)
    async def refresh_live_status(self, _stamp: str = ""):
        """Copy the shared live-check answer onto each card.

        The network call lives in a server loop. This only reads that saved
        answer, then holds the lock long enough to update the cards.
        """
        try:
            live_hrefs = await asyncio.to_thread(fetch_live_hrefs, STREAM_LINKS)
        except Exception:
            # Keep whatever dots we already showed if the check fails.
            return

        live_set = set(live_hrefs)
        async with self:
            current = [{**link} for link in self.links]
            updated = [
                {**link, "is_live": link["href"] in live_set} for link in current
            ]
            # Skip the save when nothing went live or offline.
            if updated != current:
                self.links = updated
