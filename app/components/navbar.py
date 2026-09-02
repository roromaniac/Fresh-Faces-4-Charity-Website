import reflex as rx

from app.states.nav_state import NavLink, NavState


def _desktop_link(link: NavLink) -> rx.Component:
    # Keep all element sizes the same as before (icons, text) for right-side consistency.
    return rx.el.a(
        rx.icon(
            link["icon"],
            class_name=rx.cond(
                NavState.active_href == link["href"],
                "h-3.5 w-3.5 text-amber-200",
                "h-3.5 w-3.5 text-sky-200/60 group-hover:text-amber-200",
            ),
        ),
        rx.el.span(link["label"]),
        rx.el.span(
            class_name=rx.cond(
                NavState.active_href == link["href"],
                "absolute inset-x-3 -bottom-px h-0.5 rounded-full bg-gradient-to-r from-sky-400 via-amber-200 to-amber-300",
                "absolute inset-x-3 -bottom-px h-0.5 rounded-full bg-transparent",
            )
        ),
        href=link["href"],
        on_click=lambda: NavState.select_link(link["href"]),
        class_name=rx.cond(
            NavState.active_href == link["href"],
            "ff-shimmer ff-menu-bold-font group relative flex items-center gap-1.5 overflow-hidden rounded-lg bg-white/10 px-2.5 py-1.5 text-[13px] font-semibold uppercase tracking-[0.08em] text-white transition-all duration-300 hover:scale-105",
            "ff-shimmer ff-menu-font group relative flex items-center gap-1.5 overflow-hidden rounded-lg px-2.5 py-1.5 text-[13px] font-medium uppercase tracking-[0.08em] text-sky-50 transition-all duration-300 hover:scale-105 hover:bg-white/10",
        ),
    )


def _mobile_link(link: NavLink) -> rx.Component:
    # Keep all element sizes the same for mobile links
    return rx.el.a(
        rx.el.span(
            rx.icon(
                link["icon"],
                class_name=rx.cond(
                    NavState.active_href == link["href"],
                    "h-4 w-4 text-slate-900",
                    "h-4 w-4 text-sky-200",
                ),
            ),
            class_name=rx.cond(
                NavState.active_href == link["href"],
                "flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-amber-200 to-amber-400",
                "flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/5",
            ),
        ),
        rx.el.span(link["label"], class_name="flex-1 text-left"),
        rx.icon("chevron-right", class_name="h-4 w-4 text-sky-100/40"),
        href=link["href"],
        on_click=lambda: NavState.select_link(link["href"]),
        class_name=rx.cond(
            NavState.active_href == link["href"],
            "ff-menu-bold-font flex w-full items-center gap-3 rounded-2xl border border-amber-200/30 bg-white/10 px-3 py-3 text-base font-semibold uppercase tracking-[0.06em] text-white transition-colors",
            "ff-shimmer ff-menu-font relative flex w-full items-center gap-3 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] px-3 py-3 text-base font-medium uppercase tracking-[0.06em] text-sky-50 transition-all duration-300 hover:scale-[1.02] hover:border-sky-300/40 hover:bg-white/10",
        ),
    )


def brand_mark() -> rx.Component:
    # The logo should fully cover the nav bar height: set h-full and object-contain.
    return rx.el.div(
        rx.image(
            src="/FF4LogoIntegrated2Transparent.png",
            alt="Fresh Faces 4 Logo",
            class_name="h-full w-auto object-contain",  # Take full navbar height
        ),
        class_name="flex items-center gap-2.5 h-full",  # h-full to inherit the height of its parent
    )


def _mobile_menu() -> rx.Component:
    # No size changes here; keep as before.
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Navigate the night",
                class_name="ff-data-font text-[10px] font-bold uppercase tracking-[0.28em] text-amber-200/80",
            ),
            rx.el.nav(
                rx.foreach(NavState.links, _mobile_link),
                class_name="mt-4 flex flex-col gap-2",
            ),
            rx.el.div(
                rx.el.div(class_name="h-1.5 w-20 rounded-full bg-sky-400/80"),
                rx.el.div(class_name="h-1.5 w-20 rounded-full bg-amber-300/90"),
                class_name="mt-6 flex flex-col gap-1.5",
            ),
            class_name="max-h-[calc(100dvh-3.5rem)] overflow-y-auto border-t border-white/10 bg-slate-950/95 px-5 pb-8 pt-5 backdrop-blur-xl",
        ),
        rx.el.div(
            on_click=NavState.close_menu,
            class_name="h-[calc(100dvh-3.5rem)] w-full bg-slate-950/60",
        ),
        class_name="md:hidden absolute inset-x-0 top-full flex flex-col",
    )


def navbar() -> rx.Component:
    # Navbar height is 1.75x larger: h-14 * 1.75 ~ h-24.5, Tailwind rounds to h-24 (6rem = 96px) for simplicity.
    # We use h-24 for the header container. This lets the logo be h-full.
    # On the right: keep all elements at their original size (via unchanged classes), but vertically center with the larger bar (items-center).
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                brand_mark(),
                href="/",
                on_click=lambda: NavState.select_link("/"),
                class_name="shrink-0 rounded-xl transition-transform duration-300 hover:scale-105 h-full flex items-center",  # h-full to match parent, center logo
            ),
            rx.el.nav(
                rx.foreach(NavState.links, _desktop_link),
                class_name="hidden md:flex ml-auto items-center gap-1",
            ),
            rx.el.button(
                rx.link("DONATE HERE", href="https://tiltify.com/@roromaniac8/fresh-faces-4", class_name="text-white"),
                class_name="bg-gradient-to-b from-blue-500 to-yellow-500 text-white !text-white text-xs font-bold py-2 px-4 rounded-md hover:from-blue-600 hover:to-yellow-600 transition-colors duration-200 [text-shadow:_1px_1px_2px_black,_0_0_1px_black]",
            ),
            rx.el.button(
                rx.link("RSVP TO FF4", href="https://docs.google.com/forms/d/e/1FAIpQLSeajRfsMMfNPaQdOEPPm7LjlP6Unzic2ehwbokVVxvgho5Yig/viewform?usp=header", class_name="text-white"),
                class_name="bg-gradient-to-b from-blue-500 to-yellow-500 text-white !text-white text-xs font-bold py-2 px-4 rounded-md hover:from-blue-600 hover:to-yellow-600 transition-colors duration-200 [text-shadow:_1px_1px_2px_black,_0_0_1px_black]",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        NavState.mobile_open,
                        rx.icon("x", class_name="h-5 w-5"),
                        rx.icon("menu", class_name="h-5 w-5"),
                    ),
                    on_click=NavState.toggle_menu,
                    aria_label="Toggle navigation menu",
                    aria_expanded=NavState.mobile_open,
                    class_name="md:hidden rounded-lg border border-white/15 bg-white/5 p-2 text-sky-50 transition-all duration-300 hover:scale-110 hover:bg-white/10 hover:shadow-[0_0_18px_rgba(250,204,21,0.35)]",
                ),
                class_name="ml-auto flex items-center gap-3 md:ml-0",
            ),
            class_name="flex h-24 w-full items-center gap-4 px-5 lg:px-8",  # h-24 (1.75x), items-center for vertical centering
        ),
        rx.cond(NavState.mobile_open, _mobile_menu(), rx.fragment()),
        class_name="sticky top-0 z-50 w-full border-b border-white/10 bg-slate-950/70 backdrop-blur-xl",
    )
