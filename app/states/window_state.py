from typing import TypedDict

import reflex as rx


class WindowItem(TypedDict):
    image: str
    label: str
    highlight: str
    bottom_text: str


# Note: Changed 'icon' to 'image' and replaced the values with corresponding image paths (assumes images exist in 'assets' or public directory).
LEFT_ITEMS: list[WindowItem] = [
    WindowItem(
        image="/og_skraxx.png",
        label="FF4 Partner",
        highlight="OG_Skraxx",
        bottom_text='New Video: "The Worst Trophy in EVERY Kingdom Hearts Game", Releasing 9/30!',
    ),
    WindowItem(
        image="/bioroxas.png",
        label="FF4 Partner",
        highlight="Bioroxas",
        bottom_text='New Entry in "The Psychology Of Series" Breaking into FFXIV!',
    ),
    WindowItem(
        image="/khguides.png",
        label="FF4 Partner",
        highlight="KHGGuides",
        bottom_text="Attend ReConnect 2027! The largest KH community event!",
    ),
    WindowItem(
        image="/radiantgardeners.png",
        label="FF4 Partner",
        highlight="RadiantGardeners",
        bottom_text="Play their game: The Hallowed Garden!",
    ),
    WindowItem(
        image="/nobodydaxian.png",
        label="FF4 Partner",
        highlight="NobodyDaxian",
        bottom_text="Click to check out NobodyDaxian's latest project: [INSERT HERE].",
    ),
    WindowItem(
        image="/lanzthemaster.jpg",
        label="FF4 Partner",
        highlight="LanzTheMaster",
        bottom_text="Click to check out LanzTheMaster's FULL KH2 Superboss No Damage w/ Restrictions Series!",
    ),
]

RIGHT_ITEMS: list[WindowItem] = [
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="T-Shirt",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Hoodie",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Cap",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Playing Cards",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
    ),
]


class WindowState(rx.State):
    rotate_ms: int = 10000
    left_index: int = 0
    right_index: int = 0

    @rx.var
    def left_item(self) -> WindowItem:
        return LEFT_ITEMS[self.left_index % len(LEFT_ITEMS)]

    @rx.var
    def right_item(self) -> WindowItem:
        return RIGHT_ITEMS[self.right_index % len(RIGHT_ITEMS)]

    @rx.event
    def rotate_windows(self):
        self.left_index = (self.left_index + 1) % len(LEFT_ITEMS)
        self.right_index = (self.right_index + 1) % len(RIGHT_ITEMS)

    @rx.event
    def next_left(self):
        self.left_index = (self.left_index + 1) % len(LEFT_ITEMS)

    @rx.event
    def next_right(self):
        self.right_index = (self.right_index + 1) % len(RIGHT_ITEMS)
   