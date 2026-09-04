import math

import reflex as rx

from app.components.stained_windows import (
    left_window,
    right_window,
    window_rotation_timer,
)
from app.components.supporters import supporter_wall
from app.states.event_state import EventState
from app.states.visit_state import VisitState


# Same period, amplitude, and phase so every fold stays evenly spaced.
# The strip is two identical halves; CSS slides it by 50% to loop cleanly.
_SILK_COPIES = 4
_SILK_PERIOD = 1000
_SILK_HEIGHT = 800
_SILK_AMP = 32
# Even vertical rhythm: one fold every 90 units, centered on the horizon.
_SILK_ROWS = (220, 310, 400, 490, 580)


def _silk_wave(
    y: int,
    amp: int = _SILK_AMP,
    period: int = _SILK_PERIOD,
    copies: int = _SILK_COPIES,
) -> str:
    """A looping sine fold. Every line uses this same shape so gaps stay even."""
    total = period * copies
    steps = 64 * copies
    parts: list[str] = []
    for i in range(steps + 1):
        x = total * i / steps
        t = 2 * math.pi * (x / period)
        yy = y + amp * math.sin(t)
        cmd = "M" if i == 0 else "L"
        parts.append(f"{cmd}{x:.1f},{yy:.1f}")
    return " ".join(parts)


def _silk_fill_above(y: int) -> str:
    span = _SILK_PERIOD * _SILK_COPIES
    return f"{_silk_wave(y)} L{span},0 L0,0 Z"


def _silk_fill_below(y: int, height: int = _SILK_HEIGHT) -> str:
    span = _SILK_PERIOD * _SILK_COPIES
    return f"{_silk_wave(y)} L{span},{height} L0,{height} Z"


def _silk_stroke(y: int, stroke: str, width: str) -> rx.Component:
    return rx.el.svg.path(
        d=_silk_wave(y),
        fill="none",
        stroke=stroke,
        stroke_width=width,
        vector_effect="non-scaling-stroke",
    )


def _flag_silk() -> rx.Component:
    # Blue above the horizon, gold below. Same wave, same speed, even gaps.
    y0, y1, y2, y3, y4 = _SILK_ROWS
    return rx.el.svg(
        rx.el.svg.path(d=_silk_fill_above(y0), fill="rgba(0, 87, 183, 0.10)"),
        rx.el.svg.path(d=_silk_fill_above(y1), fill="rgba(0, 87, 183, 0.11)"),
        rx.el.svg.path(d=_silk_fill_above(y2), fill="rgba(0, 87, 183, 0.13)"),
        rx.el.svg.path(d=_silk_fill_below(y2), fill="rgba(201, 162, 39, 0.09)"),
        rx.el.svg.path(d=_silk_fill_below(y3), fill="rgba(201, 162, 39, 0.08)"),
        rx.el.svg.path(d=_silk_fill_below(y4), fill="rgba(180, 140, 28, 0.07)"),
        _silk_stroke(y0, "rgba(147, 197, 253, 0.10)", "1.1"),
        _silk_stroke(y1, "rgba(147, 197, 253, 0.13)", "1.15"),
        _silk_stroke(y2, "rgba(186, 230, 253, 0.20)", "1.25"),
        _silk_stroke(y2, "rgba(234, 198, 79, 0.16)", "1.25"),
        _silk_stroke(y3, "rgba(234, 198, 79, 0.11)", "1.05"),
        _silk_stroke(y4, "rgba(234, 198, 79, 0.08)", "1"),
        view_box=f"0 0 {_SILK_PERIOD * _SILK_COPIES} {_SILK_HEIGHT}",
        preserve_aspect_ratio="none",
        xmlns="http://www.w3.org/2000/svg",
        aria_hidden="true",
        class_name="ff-silk-wind absolute inset-y-0 left-0 h-full w-[200%]",
    )


def _ukraine_waves() -> rx.Component:
    return rx.el.div(
        # The flag cloth: color wash, traveling folds, and a very gentle billow.
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(0,87,183,0.18)_0%,rgba(0,87,183,0.05)_38%,transparent_48%,transparent_52%,rgba(201,162,39,0.05)_62%,rgba(201,162,39,0.14)_100%)]"
            ),
            _flag_silk(),
            rx.el.div(class_name="ff-silk-drape absolute inset-0"),
            class_name="ff-flag-billow absolute inset-0",
        ),
        # Dark stage stays still so the title and windows do not breathe.
        rx.el.div(
            class_name="absolute inset-0 bg-[radial-gradient(ellipse_78%_72%_at_50%_42%,rgba(2,6,23,0.78)_0%,rgba(2,6,23,0.42)_48%,transparent_76%)]"
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


def _visitor_seal() -> rx.Component:
    return rx.el.div(
        rx.image(
            src="/KH-heart.webp",
            alt="",
            class_name="h-8 w-8 object-contain drop-shadow-[0_0_12px_rgba(250,204,21,0.55)]",
        ),
        rx.el.div(
            rx.el.p(
                VisitState.visitor_count_label,
                class_name="ff-data-font text-2xl font-bold leading-none tracking-wide text-amber-200 drop-shadow-[0_0_16px_rgba(250,204,21,0.45)] sm:text-3xl",
            ),
            rx.el.p(
                "lights visited",
                class_name="ff-menu-font text-sm tracking-[0.06em] text-sky-100/80",
            ),
        ),
        rx.image(
            src="/ukraine_heart.webp",
            alt="",
            class_name="h-8 w-8 object-contain drop-shadow-[0_0_12px_rgba(56,189,248,0.55)]",
        ),
        class_name="ff-float mt-3 flex items-center gap-3 rounded-2xl border border-white/15 bg-slate-900/50 px-4 py-2 backdrop-blur-md",
    )


def _title_block() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Fresh Faces 4",
            class_name="ff-title-font ff-title-gradient block w-full whitespace-nowrap text-center text-[9vw] font-bold leading-[1.08] tracking-tight drop-shadow-[0_0_28px_rgba(56,189,248,0.35)] sm:text-[7.5vw] md:text-[3.1vw] lg:text-[3.4vw] xl:text-6xl",
        ),
        rx.el.p(
            "A KH2 Rando Charity Production",
            rx.el.br(),
            "for Project Hope",
            class_name="ff-gummi-font text-center text-base tracking-[0.08em] text-sky-100/80 uppercase sm:text-lg",
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
        _visitor_seal(),
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
            # Desktop layout: grid with [1fr auto 1fr] so sides get extra space.
            rx.el.div(
                rx.el.div(
                    left_window(),
                    class_name="hidden w-full min-w-0 items-center justify-center md:flex",
                ),
                _hero_shrine(),
                rx.el.div(
                    right_window(),
                    class_name="hidden w-full min-w-0 items-center justify-center md:flex",
                ),
                # Main change: grid-cols-[1fr_auto_1fr] instead of [auto_1fr_auto]
                class_name=(
                    "hidden w-full items-center "
                    "md:grid md:grid-cols-[1fr_auto_1fr]"
                ),
            ),
            # Mobile stays unchanged
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
            # Remove max-w-6xl, mx-auto, reduce px-5/lg:px-10 for edge-to-edge
            class_name="relative flex w-full flex-col items-center gap-4 py-3 lg:gap-6 px-2 lg:px-4",
        ),
        id="home",
        custom_attrs={"aria-label": EventState.event_name},
        class_name="relative flex w-full flex-1 items-center overflow-hidden bg-slate-950",
    )
