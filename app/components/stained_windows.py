import reflex as rx

from app.states.window_state import WindowItem, WindowState


def _dots(count: int, active: int) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(count),
            lambda i: rx.el.span(
                class_name=rx.cond(
                    i == active,
                    "h-1.5 w-4 rounded-full bg-amber-200/90 transition-all duration-500",
                    "h-1.5 w-1.5 rounded-full bg-white/25 transition-all duration-500",
                )
            ),
        ),
        class_name="flex items-center justify-center gap-1",
    )


def _pane(item: WindowItem, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            item["division"],
            class_name=rx.cond(
                item["accent"] == "amber",
                "ff-data-font text-[10px] uppercase tracking-[0.22em] text-amber-200/90",
                "ff-data-font text-[10px] uppercase tracking-[0.22em] text-sky-200/90",
            ),
        ),
        rx.el.div(
            rx.icon(
                item["icon"],
                class_name=rx.cond(
                    item["accent"] == "amber",
                    "h-9 w-9 text-amber-200 drop-shadow-[0_0_18px_rgba(250,204,21,0.75)] lg:h-10 lg:w-10",
                    "h-9 w-9 text-sky-200 drop-shadow-[0_0_18px_rgba(125,211,252,0.75)] lg:h-10 lg:w-10",
                ),
            ),
            class_name=rx.cond(
                item["accent"] == "amber",
                "flex h-16 w-16 items-center justify-center rounded-xl border border-amber-200/30 bg-amber-300/10 lg:h-18 lg:w-18",
                "flex h-16 w-16 items-center justify-center rounded-xl border border-sky-200/30 bg-sky-400/10 lg:h-18 lg:w-18",
            ),
        ),
        rx.el.p(
            item["label"],
            class_name="ff-title-font text-center text-base leading-tight text-white lg:text-lg",
        ),
        rx.el.p(
            item["caption"],
            class_name="ff-menu-font text-center text-[11px] leading-snug text-sky-100/70 lg:text-xs",
        ),
        key=index,
        class_name="ff-pane-in flex h-full w-full flex-col items-center justify-center gap-2 px-4 pb-5",
    )


def stained_window(
    item: WindowItem,
    index: int,
    count: int,
    on_click: rx.event.EventType,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="pointer-events-none absolute -inset-2 rounded-3xl bg-[conic-gradient(from_0deg,rgba(56,189,248,0.30),rgba(250,204,21,0.30),rgba(99,102,241,0.30),rgba(56,189,248,0.30))] blur-[10px] opacity-60 transition-opacity duration-500 group-hover:opacity-95"
        ),
        rx.el.div(
            rx.el.div(
                class_name="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:22px_22px] opacity-50"
            ),
            rx.el.div(
                class_name="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.14),transparent_60%)]"
            ),
            rx.el.div(
                _pane(item, index),
                rx.el.div(
                    _dots(count, index),
                    class_name="absolute inset-x-0 bottom-2 flex justify-center",
                ),
                class_name="relative h-full w-full",
            ),
            class_name="ff-glass-window relative h-full w-full overflow-hidden rounded-2xl border border-white/15 bg-slate-900/60 backdrop-blur-md",
        ),
        on_click=on_click,
        class_name="group relative aspect-square w-40 shrink-0 cursor-pointer p-1 transition-transform duration-500 hover:scale-[1.04] sm:w-44 md:w-48 lg:w-60 xl:w-[17rem]",
        style={"max_width": "100%"},
    )


def left_window() -> rx.Component:
    return stained_window(
        WindowState.left_item,
        WindowState.left_index,
        4,
        WindowState.next_left,
    )


def right_window() -> rx.Component:
    return stained_window(
        WindowState.right_item,
        WindowState.right_index,
        4,
        WindowState.next_right,
    )


def window_rotation_timer() -> rx.Component:
    return rx.moment(
        interval=WindowState.rotate_ms,
        on_change=WindowState.rotate_windows,
        class_name="hidden",
    )
