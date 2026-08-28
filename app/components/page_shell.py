"""Shared chrome for inner pages: navbar, stream bar, and a night-sky frame."""

import reflex as rx

from app.components.navbar import navbar
from app.components.stream_bar import stream_bar


def _page_sky() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="ff-glow absolute -top-40 left-1/2 h-[28rem] w-[28rem] -translate-x-1/2 rounded-full bg-sky-500/20"
        ),
        rx.el.div(
            class_name="ff-glow absolute -bottom-48 right-1/4 h-[24rem] w-[24rem] rounded-full bg-amber-400/15 [animation-delay:2.5s]"
        ),
        rx.el.div(
            class_name="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.08),transparent_55%)]"
        ),
        class_name="pointer-events-none absolute inset-0 overflow-hidden",
    )


def page_shell(*children: rx.Component) -> rx.Component:
    return rx.el.main(
        navbar(),
        stream_bar(),
        rx.el.div(
            _page_sky(),
            rx.el.div(
                *children,
                class_name="relative mx-auto flex w-full max-w-6xl flex-1 flex-col px-5 py-8 lg:px-8 lg:py-10",
            ),
            class_name="relative flex w-full flex-1 flex-col overflow-y-auto",
        ),
        class_name="ff-body flex h-dvh w-full flex-col overflow-hidden bg-slate-950 text-sky-50",
    )


def page_heading(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            title,
            class_name="ff-title-font ff-title-gradient text-center text-4xl font-bold tracking-tight sm:text-5xl",
        ),
        rx.el.p(
            subtitle,
            class_name="ff-script-font mt-2 text-center text-base text-sky-100/80 sm:text-lg",
        ),
        rx.el.div(
            rx.el.div(class_name="h-1.5 w-24 rounded-full bg-sky-400/80"),
            rx.el.div(class_name="h-1.5 w-24 rounded-full bg-amber-300/90"),
            class_name="mx-auto mt-4 flex w-fit flex-col gap-1",
        ),
        class_name="mb-8 flex flex-col items-center",
    )
