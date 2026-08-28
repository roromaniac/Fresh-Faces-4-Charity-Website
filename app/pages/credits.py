from typing import TypedDict

import reflex as rx

from app.components.page_shell import page_heading, page_shell


class Credit(TypedDict):
    name: str
    role: str
    role_class: str
    twitch_channel: str
    icon: str


# Local credits list. Add people here as the FF4 team grows.
CREDITS: list[Credit] = [
    {
        "name": "roromaniac",
        "role": "Director",
        "role_class": "Host",
        "twitch_channel": "https://www.twitch.tv/roromaniac8",
        "icon": "crown",
    },
]


def _credit_card(credit: Credit) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.icon(credit["icon"], class_name="h-8 w-8 text-amber-200"),
            class_name="flex h-16 w-16 items-center justify-center rounded-full border border-amber-200/40 bg-amber-300/10",
        ),
        rx.el.a(
            rx.icon("twitch", class_name="h-4 w-4 text-purple-300"),
            credit["name"],
            href=credit["twitch_channel"],
            target="_blank",
            class_name="ff-menu-bold-font mt-3 flex items-center gap-2 text-amber-100 transition-colors hover:text-amber-200",
        ),
        rx.el.p(
            credit["role"],
            class_name="ff-script-font mt-1 text-center text-sky-100/80",
        ),
        rx.el.p(
            credit["role_class"],
            class_name="ff-data-font mt-3 rounded-full border border-amber-200/30 bg-amber-200/15 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-amber-100",
        ),
        class_name="flex flex-col items-center rounded-2xl border border-white/10 bg-white/[0.04] p-6 backdrop-blur-md transition-transform duration-300 hover:-translate-y-1 hover:border-sky-300/40",
    )


def credits() -> rx.Component:
    return page_shell(
        page_heading(
            "The Friends that Power Fresh Faces 4",
            "Thank the people who made this night possible",
        ),
        rx.el.div(
            rx.foreach(CREDITS, _credit_card),
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4",
        ),
    )
