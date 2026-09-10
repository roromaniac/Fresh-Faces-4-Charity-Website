import asyncio
from typing import TypedDict

import reflex as rx


class WindowItem(TypedDict):
    image: str
    label: str
    highlight: str
    bottom_text: str
    href: str


# Note: Changed 'icon' to 'image' and replaced the values with corresponding image paths (assumes images exist in 'assets' or public directory).
LEFT_ITEMS: list[WindowItem] = [
    WindowItem(
        image="/og_skraxx.png",
        label="FF4 Partner",
        highlight="OG_Skraxx",
        bottom_text='New Video: "The Worst Trophy in EVERY Kingdom Hearts Game", Releasing 9/30!',
        href="https://www.youtube.com/@ogskraxx6678",
    ),
    WindowItem(
        image="/bioroxas.png",
        label="FF4 Partner",
        highlight="Bioroxas",
        bottom_text='New Entry in "The Psychology Of Series" Breaking into FFXIV!',
        href="https://www.youtube.com/@BioRoxas",
    ),
    WindowItem(
        image="/khguides.png",
        label="FF4 Partner",
        highlight="KHGGuides",
        bottom_text="Attend ReConnect 2027! The largest KH community event!",
        href="https://khreconnect.com",
    ),
    WindowItem(
        image="/radiantgardeners.png",
        label="FF4 Partner",
        highlight="RadiantGardeners",
        bottom_text="Play their game: The Hallowed Garden!",
        href="https://store.steampowered.com/app/3763380/The_Hallowed_Garden/",
    ),
    WindowItem(
        image="/nobodydaxian.png",
        label="FF4 Partner",
        highlight="NobodyDaxian",
        bottom_text="NobodyDaxian has supported Fresh Faces from inception. Check him out here!",
        href="https://www.youtube.com/@NobodyDaxian",
    ),
    WindowItem(
        image="/lanzthemaster.jpg",
        label="FF4 Partner",
        highlight="LanzTheMaster",
        bottom_text="Click to check out LanzTheMaster's FULL KH2 Superboss No Damage w/ Restrictions Series!",
        href="https://www.youtube.com/@lanzthemaster",
    ),
]

RIGHT_ITEMS: list[WindowItem] = [
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="T-Shirt",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
        href="",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Hoodie",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
        href="",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Cap",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
        href="",
    ),
    WindowItem(
        image="/coming_soon.png",
        label="Merch Showcase",
        highlight="Playing Cards",
        bottom_text="ALL profits go to Project Hope's Ukraine relief fund.",
        href="",
    ),
]


class WindowState(rx.State):
    rotate_ms: int = 7500
    left_index: int = 0
    right_index: int = 0
    # Bumps on each arrow click so the background rotator restarts its wait.
    pause_token: int = 0
    rotator_running: bool = False

    @rx.var
    def left_item(self) -> WindowItem:
        return LEFT_ITEMS[self.left_index % len(LEFT_ITEMS)]

    @rx.var
    def right_item(self) -> WindowItem:
        return RIGHT_ITEMS[self.right_index % len(RIGHT_ITEMS)]

    def _restart_timer(self):
        self.pause_token += 1

    def _advance_both(self):
        self.left_index = (self.left_index + 1) % len(LEFT_ITEMS)
        self.right_index = (self.right_index + 1) % len(RIGHT_ITEMS)

    @rx.event(background=True)
    async def start_rotator(self, _stamp: str = ""):
        # One loop per session. It sleeps 10s, then rotates unless an arrow
        # click changed pause_token during that wait (timer reset).
        async with self:
            if self.rotator_running:
                return
            self.rotator_running = True
        while True:
            async with self:
                token = self.pause_token
                delay = self.rotate_ms / 1000
            await asyncio.sleep(delay)
            async with self:
                if self.pause_token != token:
                    continue
                self._advance_both()

    @rx.event
    def next_left(self):
        self.left_index = (self.left_index + 1) % len(LEFT_ITEMS)
        self._restart_timer()

    @rx.event
    def prev_left(self):
        self.left_index = (self.left_index - 1) % len(LEFT_ITEMS)
        self._restart_timer()

    @rx.event
    def next_right(self):
        self.right_index = (self.right_index + 1) % len(RIGHT_ITEMS)
        self._restart_timer()

    @rx.event
    def prev_right(self):
        self.right_index = (self.right_index - 1) % len(RIGHT_ITEMS)
        self._restart_timer()

   