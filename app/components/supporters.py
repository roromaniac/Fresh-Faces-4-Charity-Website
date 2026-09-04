import reflex as rx

from app.states.event_state import EventState, Partner


def _partner_logo(partner: Partner, mark_class: str, **props) -> rx.Component:
    """One logo in the row. Names live in alt text so the banner stays image-only."""
    return rx.el.div(
        rx.image(
            src=partner["image"],
            alt=partner["name"],
            title=partner["name"],
            class_name=mark_class,
        ),
        class_name="group flex items-center justify-center",
        **props,
    )


def _partner_banner(title: str, partners: rx.Var, mark_class: str) -> rx.Component:
    """Yellow centered heading with a single centered row of logos under it."""
    return rx.el.section(
        rx.el.h2(
            title,
            class_name=(
                "ff-menu-bold-font text-center text-xl font-bold tracking-wide "
                "text-yellow-300 drop-shadow-[0_2px_10px_rgba(250,204,21,0.35)] "
                "sm:text-2xl md:text-3xl"
            ),
        ),
        rx.el.div(
            rx.foreach(
                partners,
                lambda p: _partner_logo(p, mark_class, key=p["name"]),
            ),
            class_name=(
                "flex w-full flex-wrap items-center justify-center "
                "gap-x-8 gap-y-5 sm:gap-x-12 md:gap-x-16"
            ),
        ),
        class_name="flex w-full flex-col items-center gap-5 sm:gap-6",
    )


def supporter_wall() -> rx.Component:
    return rx.el.div(
        _partner_banner(
            "Presented in Collaboration with:",
            EventState.collaborators,
            "h-14 w-auto max-h-14 max-w-[8.5rem] object-contain brightness-125 drop-shadow-[0_0_14px_rgba(125,211,252,0.35)] drop-shadow-[0_8px_18px_rgba(0,0,0,0.55)] transition-transform duration-300 group-hover:scale-110 sm:h-16 sm:max-h-16 sm:max-w-[10rem] md:h-20 md:max-h-20 md:max-w-[12rem]",
        ),
        # No sponsors to announce yet. Uncomment this block when they are ready.
        # _partner_banner(
        #     "Sponsored By:",
        #     EventState.sponsors,
        #     "h-16 w-auto max-h-16 max-w-[14rem] object-contain brightness-125 drop-shadow-[0_0_14px_rgba(125,211,252,0.35)] drop-shadow-[0_8px_18px_rgba(0,0,0,0.55)] transition-transform duration-300 group-hover:scale-110 sm:h-20 sm:max-h-20 sm:max-w-[16rem] md:h-24 md:max-h-24 md:max-w-[18rem]",
        # ),
        class_name="flex w-full max-w-6xl flex-col items-center gap-10 py-2 md:gap-12",
    )
