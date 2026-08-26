from typing import TypedDict

import reflex as rx


class WindowItem(TypedDict):
    icon: str
    label: str
    division: str
    caption: str
    accent: str


class WindowState(rx.State):
    rotate_ms: int = 10000
    left_index: int = 0
    right_index: int = 0

    left_items: list[WindowItem] = [
        {
            "icon": "mic-vocal",
            "label": "Vocal Division",
            "division": "Division I",
            "caption": "Eight new voices open the stage.",
            "accent": "sky",
        },
        {
            "icon": "guitar",
            "label": "Strings & Bands",
            "division": "Division II",
            "caption": "Live sets mixed by Sunflower Sound.",
            "accent": "amber",
        },
        {
            "icon": "palette",
            "label": "Stained Glass Art",
            "division": "Division III",
            "caption": "Ribbon arcs painted for Ukraine.",
            "accent": "sky",
        },
        {
            "icon": "sparkles",
            "label": "Fresh Debuts",
            "division": "Spotlight",
            "caption": "Twenty-four first-time performers.",
            "accent": "amber",
        },
    ]

    right_items: list[WindowItem] = [
        {
            "icon": "heart-handshake",
            "label": "100% Donated",
            "division": "Relief",
            "caption": "Every ticket becomes aid.",
            "accent": "amber",
        },
        {
            "icon": "calendar-days",
            "label": "June 14 · 5 PM",
            "division": "Showtime",
            "caption": "Doors open one hour early.",
            "accent": "sky",
        },
        {
            "icon": "radio",
            "label": "Livestreamed",
            "division": "Worldwide",
            "caption": "Six cameras, Twitch & YouTube.",
            "accent": "amber",
        },
        {
            "icon": "landmark",
            "label": "The Lumen Hall",
            "division": "Venue",
            "caption": "Costs covered by Harbor Bank.",
            "accent": "sky",
        },
    ]

    @rx.var
    def left_item(self) -> WindowItem:
        return self.left_items[self.left_index % len(self.left_items)]

    @rx.var
    def right_item(self) -> WindowItem:
        return self.right_items[self.right_index % len(self.right_items)]

    @rx.event
    def rotate_windows(self):
        self.left_index = (self.left_index + 1) % len(self.left_items)
        self.right_index = (self.right_index + 1) % len(self.right_items)

    @rx.event
    def next_left(self):
        self.left_index = (self.left_index + 1) % len(self.left_items)

    @rx.event
    def next_right(self):
        self.right_index = (self.right_index + 1) % len(self.right_items)
