import reflex as rx

from app.components.stained_windows import (
    left_window,
    right_window,
    window_rotation_timer,
)
from app.components.supporters import supporter_wall
from app.states.event_state import EventState


def _ukraine_waves() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="ff-glow absolute -top-40 left-1/2 h-[34rem] w-[34rem] -translate-x-1/2 rounded-full bg-sky-500/25"
        ),
        rx.el.div(
            class_name="ff-glow absolute -bottom-48 left-1/3 h-[30rem] w-[30rem] rounded-full bg-amber-400/20 [animation-delay:2.5s]"
        ),
        rx.el.div(
            class_name="ff-wave absolute inset-x-[-20%] bottom-1/3 h-64 rounded-[100%] bg-gradient-to-t from-sky-500/35 via-sky-400/15 to-transparent blur-2xl"
        ),
        rx.el.div(
            class_name="ff-wave-alt absolute inset-x-[-20%] bottom-0 h-72 rounded-[100%] bg-gradient-to-t from-amber-300/30 via-amber-200/12 to-transparent blur-2xl"
        ),
        rx.el.div(
            class_name="ff-wave absolute inset-x-[-25%] bottom-16 h-40 rounded-[100%] border-t border-sky-200/25 [animation-delay:1.5s]"
        ),
        rx.el.div(
            class_name="absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,rgba(255,255,255,0.10),transparent_55%)]"
        ),
        rx.el.div(
            class_name="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:64px_64px] opacity-40"
        ),
        class_name="pointer-events-none absolute inset-0 overflow-hidden",
    )


def _logo_image() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 rounded-full bg-[conic-gradient(from_0deg,rgba(56,189,248,0.35),rgba(250,204,21,0.35),rgba(99,102,241,0.35),rgba(56,189,248,0.35))] blur-[6px] opacity-70 transition-opacity duration-500 group-hover:opacity-100"
        ),
        rx.image(
            src=EventState.logo_image,
            alt=EventState.event_name,
            class_name="relative h-full w-full rounded-full object-contain transition-transform duration-500 group-hover:scale-105",
        ),
        class_name="ff-float group relative h-28 w-28 shrink-0 cursor-pointer rounded-full border border-white/15 bg-slate-900/50 p-1.5 backdrop-blur-md transition-all duration-500 hover:scale-105 hover:shadow-[0_0_60px_rgba(56,189,248,0.35)] sm:h-36 sm:w-36 md:h-28 md:w-28 lg:h-36 lg:w-36 xl:h-44 xl:w-44",
    )


def _logo_artwork() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 rounded-full border border-amber-200/30 animate-[spin_30s_linear_infinite] group-hover:border-amber-200/70"
        ),
        rx.el.div(
            class_name="absolute inset-3 rounded-full border border-sky-300/25 animate-[spin_20s_linear_infinite_reverse]"
        ),
        rx.el.div(
            class_name="absolute inset-0 rounded-full bg-[conic-gradient(from_0deg,rgba(56,189,248,0.25),rgba(250,204,21,0.25),rgba(99,102,241,0.25),rgba(56,189,248,0.25))] blur-[3px] opacity-70 transition-opacity duration-500 group-hover:opacity-100"
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("crown", class_name="h-4 w-4 text-slate-900"),
                class_name="mb-1 flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-amber-200 to-amber-400 transition-transform duration-300 group-hover:-translate-y-1",
            ),
            rx.icon(
                EventState.logo_icon,
                class_name="h-14 w-14 text-sky-200 drop-shadow-[0_0_26px_rgba(125,211,252,0.9)] transition-transform duration-500 group-hover:scale-110 sm:h-16 sm:w-16",
            ),
            rx.icon(
                "key-round",
                class_name="mt-1 h-5 w-5 text-amber-200/80 transition-transform duration-500 group-hover:rotate-12",
            ),
            class_name="absolute inset-0 flex flex-col items-center justify-center",
        ),
        class_name="ff-float group relative h-28 w-28 shrink-0 cursor-pointer rounded-full border border-dashed border-white/15 bg-slate-900/50 backdrop-blur-md transition-all duration-500 hover:scale-105 hover:shadow-[0_0_60px_rgba(56,189,248,0.35)] sm:h-36 sm:w-36 md:h-28 md:w-28 lg:h-36 lg:w-36 xl:h-44 xl:w-44",
    )


def _logo_mark() -> rx.Component:
    return rx.cond(
        EventState.logo_image != "",
        _logo_image(),
        rx.cond(EventState.logo_icon != "", _logo_artwork(), rx.fragment()),
    )


def _title_block() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Fresh Faces 4",
            class_name="ff-title-font ff-title-gradient block w-full whitespace-nowrap text-center text-[9vw] font-bold leading-[1.08] tracking-tight drop-shadow-[0_0_28px_rgba(56,189,248,0.35)] sm:text-[7.5vw] md:text-[3.1vw] lg:text-[3.4vw] xl:text-6xl",
        ),
        rx.el.p(
            EventState.tagline,
            class_name="ff-script-font text-center text-base tracking-[0.08em] text-sky-100/80 sm:text-lg",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-1.5 w-24 rounded-full bg-sky-400/80 transition-all duration-500 group-hover:w-32"
            ),
            rx.el.div(
                class_name="h-1.5 w-24 rounded-full bg-amber-300/90 transition-all duration-500 group-hover:w-32"
            ),
            class_name="group mx-auto flex w-fit cursor-pointer flex-col gap-1",
        ),
        class_name="flex flex-col items-center gap-2",
    )


def _hero_shrine() -> rx.Component:
    return rx.el.div(
        _logo_mark(),
        _title_block(),
        class_name="flex min-w-0 flex-col items-center justify-center gap-3 text-center",
    )


def poster() -> rx.Component:
    return rx.el.section(
        _ukraine_waves(),
        window_rotation_timer(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    left_window(),
                    class_name="hidden min-w-0 items-center justify-center md:flex",
                ),
                _hero_shrine(),
                rx.el.div(
                    right_window(),
                    class_name="hidden min-w-0 items-center justify-center md:flex",
                ),
                class_name="hidden w-full items-center md:grid md:grid-cols-3",
            ),
            rx.el.div(
                _hero_shrine(),
                rx.el.div(
                    left_window(),
                    right_window(),
                    class_name="flex w-full items-start justify-center gap-4 sm:gap-6",
                ),
                class_name="flex w-full flex-col items-center gap-4 md:hidden",
            ),
            rx.el.div(
                supporter_wall(),
                class_name="flex w-full justify-center",
            ),
            class_name="relative mx-auto flex w-full max-w-6xl flex-col items-center gap-4 px-5 py-3 lg:gap-6 lg:px-10",
        ),
        id="home",
        custom_attrs={"aria-label": EventState.event_name},
        class_name="relative flex w-full flex-1 items-center overflow-hidden bg-slate-950",
    )
