import reflex as rx

from app.states.event_state import EventState, Partner


def _supporter_mark(partner: Partner) -> rx.Component:
    return rx.cond(
        partner["image"] != "",
        rx.el.div(
            rx.image(
                src=partner["image"],
                alt=partner["name"],
                class_name="h-full w-full rounded-full object-cover transition-transform duration-300 group-hover:scale-110",
            ),
            class_name="flex h-6 w-6 shrink-0 items-center justify-center overflow-hidden rounded-full border border-white/15 bg-white/[0.06] transition-all duration-300 group-hover:border-amber-200/60 group-hover:shadow-[0_0_18px_rgba(250,204,21,0.45)]",
        ),
        rx.cond(
            partner["icon"] != "",
            rx.el.div(
                rx.icon(
                    partner["icon"],
                    class_name="h-3.5 w-3.5 text-amber-200/90 transition-transform duration-300 group-hover:scale-125 group-hover:text-amber-100",
                ),
                class_name="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-white/15 bg-white/[0.06] transition-all duration-300 group-hover:border-amber-200/60 group-hover:bg-amber-200/15 group-hover:shadow-[0_0_18px_rgba(250,204,21,0.45)]",
            ),
            rx.fragment(),
        ),
    )


def _supporter_tile(partner: Partner, **props) -> rx.Component:
    return rx.el.div(
        _supporter_mark(partner),
        rx.el.p(
            partner["name"],
            class_name="ff-menu-bold-font truncate text-[11px] font-semibold leading-tight text-sky-50/90 transition-colors duration-300 group-hover:text-white",
        ),
        class_name="ff-shimmer group relative flex w-full cursor-pointer items-center gap-2 overflow-hidden rounded-lg border border-white/10 bg-white/[0.03] px-2 py-1 backdrop-blur-md transition-all duration-300 hover:-translate-y-0.5 hover:scale-[1.04] hover:border-sky-300/50 hover:bg-white/[0.09] hover:shadow-[0_0_26px_rgba(56,189,248,0.35)]",
        **props,
    )


def _group_label(label: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-3 w-3 text-amber-200"),
        rx.el.h2(
            label,
            class_name="ff-data-font text-[9px] font-bold uppercase tracking-[0.26em] text-amber-200/90",
        ),
        rx.el.span(
            class_name="h-px flex-1 bg-gradient-to-r from-amber-200/40 via-sky-300/25 to-transparent"
        ),
        class_name="flex w-full items-center gap-1.5",
    )


def _supporter_group(
    label: str, icon: str, partners: rx.Var, columns: str
) -> rx.Component:
    return rx.el.div(
        _group_label(label, icon),
        rx.el.div(
            rx.foreach(partners, lambda p: _supporter_tile(p, key=p["name"])),
            class_name=columns,
        ),
        class_name="flex w-full flex-col gap-1.5",
    )


def supporter_wall() -> rx.Component:
    return rx.el.div(
        _supporter_group(
            "Collaborators",
            "users-round",
            EventState.collaborators,
            "grid grid-cols-2 gap-1.5 sm:grid-cols-3",
        ),
        _supporter_group(
            "Endorsers",
            "badge-check",
            EventState.endorsers,
            "grid grid-cols-1 gap-1.5 sm:grid-cols-3",
        ),
        _supporter_group(
            "Sponsors",
            "crown",
            EventState.sponsors,
            "grid grid-cols-2 gap-1.5 sm:grid-cols-4",
        ),
        class_name="flex w-full max-w-3xl flex-col gap-2.5",
    )
