from typing import TypedDict

import reflex as rx


class StreamLink(TypedDict):
    label: str
    caption: str
    href: str
    platform: str
    icon: str
    wordmark: str


class StreamState(rx.State):
    """Configurable stream / archive portal links.

    Swap the `href` values for the real Twitch and YouTube URLs when they are
    finalized. Safe, non-broken placeholders are used until then.
    """

    links: list[StreamLink] = [
        {
            "label": "Fresh Faces",
            "caption": "Main Bracket",
            "href": "https://www.twitch.tv/roromaniac8",
            "platform": "twitch",
            "icon": "twitch",
            "wordmark": "Twitch",
        },
        {
            "label": "Graduated Faces",
            "caption": "Alumni Stage",
            "href": "https://www.twitch.tv/WallpeSH",
            "platform": "twitch",
            "icon": "twitch",
            "wordmark": "Twitch",
        },
        {
            "label": "Veterans Division",
            "caption": "Masters Arena",
            "href": "https://www.twitch.tv/KH2FMRando",
            "platform": "twitch",
            "icon": "twitch",
            "wordmark": "Twitch",
        },
        {
            "label": "Full Matches",
            "caption": "Archive VODs",
            "href": "https://www.youtube.com/@roroKH2FMR",
            "platform": "youtube",
            "icon": "youtube",
            "wordmark": "YouTube",
        },
    ]
