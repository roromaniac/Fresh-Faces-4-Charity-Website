"""Large stained-window pages for a Twitch browser source.

Each page shows one rotator, the same cards and spin-in as the home page.
The page itself is clear so the stream shows through around the glass.
"""

import reflex as rx

from app.components.stained_windows import (
    left_window,
    right_window,
    window_rotation_timer,
)


def _overlay_page(window: rx.Component) -> rx.Component:
    # Center one window and let it fill the browser source.
    return rx.el.main(
        window_rotation_timer(),
        rx.el.div(
            window,
            class_name="ff-window-overlay-stage",
        ),
        class_name="ff-window-overlay ff-body",
    )


def left_window_high_res() -> rx.Component:
    return _overlay_page(left_window())


def right_window_high_res() -> rx.Component:
    return _overlay_page(right_window())
