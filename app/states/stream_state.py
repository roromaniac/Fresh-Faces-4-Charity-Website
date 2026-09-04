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

    # How often the bar asks Twitch / YouTube "is this channel on air?"
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
    def any_live(self) -> bool:
        return any(link["is_live"] for link in self.links)

    @rx.event(background=True)
    async def refresh_live_status(self, _stamp: str = ""):
        """Run the live-check script and store the result on each card."""
        async with self:
            snapshot = [{**link} for link in self.links]

        try:
            live_hrefs = await asyncio.to_thread(fetch_live_hrefs, snapshot)
        except Exception:
            # Keep whatever dots we already showed if the check fails.
            return

        live_set = set(live_hrefs)
        async with self:
            self.links = [
                {**link, "is_live": link["href"] in live_set} for link in self.links
            ]
