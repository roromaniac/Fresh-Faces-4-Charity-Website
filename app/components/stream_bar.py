import reflex as rx

from app.components.brand_glyphs import twitch_glyph, youtube_glyph
from app.states.stream_state import StreamLink, StreamState


def _brand_badge(link: StreamLink) -> rx.Component:
    return rx.el.span(
        rx.cond(
            link["platform"] == "twitch",
            twitch_glyph(
                "h-3.5 w-3.5 shrink-0 text-white drop-shadow-[0_0_6px_rgba(145,70,255,0.9)]"
            ),
            youtube_glyph(
                "h-3.5 w-3.5 shrink-0 text-white drop-shadow-[0_0_6px_rgba(255,0,0,0.9)]"
            ),
        ),
        rx.el.span(
            link["wordmark"],
            class_name="ff-menu-bold-font hidden text-[9px] font-bold uppercase leading-none tracking-[0.14em] text-white lg:inline",
        ),
        class_name=rx.cond(
            link["platform"] == "twitch",
            "ff-brand-badge ff-brand-badge--twitch flex shrink-0 items-center gap-1 rounded-md border border-[#b98cff]/60 bg-[#9146ff] px-1.5 py-1",
            "ff-brand-badge ff-brand-badge--youtube flex shrink-0 items-center gap-1 rounded-md border border-[#ff5b5b]/60 bg-[#ff0000] px-1.5 py-1",
        ),
    )


def _chip(link: StreamLink) -> rx.Component:
    return rx.el.a(
        _brand_badge(link),
        rx.el.span(
            rx.el.span(
                link["label"],
                class_name="ff-menu-bold-font block truncate text-[11px] font-semibold uppercase leading-none tracking-[0.1em] text-sky-50",
            ),
            rx.el.span(
                rx.el.span(
                    link["caption"],
                    class_name="ff-data-font",
                ),
                rx.el.span(
                    "·",
                    class_name="opacity-60",
                ),
                rx.el.span(
                    link["wordmark"],
                    class_name=rx.cond(
                        link["platform"] == "twitch",
                        "ff-data-font text-[#c4a6ff]",
                        "ff-data-font text-[#ff9b9b]",
                    ),
                ),
                class_name="ff-data-font mt-0.5 flex min-w-0 items-center gap-1 truncate text-[9px] uppercase leading-none tracking-[0.22em] text-amber-200/70",
            ),
            class_name="flex min-w-0 flex-col",
        ),
        href=link["href"],
        target="_blank",
        rel="noopener noreferrer",
        aria_label=f"{link['label']} on {link['wordmark']}",
        class_name=rx.cond(
            link["platform"] == "twitch",
            "ff-shimmer ff-portal-chip ff-portal-chip--twitch group relative flex w-full min-w-0 items-center gap-2 overflow-hidden rounded-xl border border-[#9146ff]/45 bg-[#9146ff]/10 px-2.5 py-1.5 transition-all duration-300 hover:scale-[1.03] hover:border-[#b98cff]/80 hover:bg-[#9146ff]/20 hover:shadow-[0_0_22px_rgba(145,70,255,0.5)] lg:w-auto lg:shrink-0",
            "ff-shimmer ff-portal-chip ff-portal-chip--youtube group relative flex w-full min-w-0 items-center gap-2 overflow-hidden rounded-xl border border-[#ff0000]/45 bg-[#ff0000]/10 px-2.5 py-1.5 transition-all duration-300 hover:scale-[1.03] hover:border-[#ff5b5b]/80 hover:bg-[#ff0000]/20 hover:shadow-[0_0_22px_rgba(255,0,0,0.45)] lg:w-auto lg:shrink-0",
        ),
    )


def stream_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-amber-200/50 to-transparent",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("radio", class_name="h-3.5 w-3.5 stroke-amber-200"),
                rx.el.span(
                    "Watch",
                    class_name="ff-data-font text-[9px] font-bold uppercase tracking-[0.3em] text-amber-200/80",
                ),
                class_name="hidden shrink-0 items-center gap-1.5 border-r border-white/10 pr-3 lg:flex",
            ),
            rx.el.div(
                rx.foreach(StreamState.links, _chip),
                class_name="grid w-full min-w-0 grid-cols-2 gap-2 lg:flex lg:flex-1 lg:flex-wrap lg:items-center",
            ),
            class_name="flex w-full flex-col gap-2 px-5 py-2.5 lg:flex-row lg:items-center lg:gap-3 lg:px-8",
        ),
        class_name="relative z-40 w-full shrink-0 border-b border-white/10 bg-slate-950/60 backdrop-blur-xl",
    )
