import reflex as rx

from app.components.page_shell import page_heading, page_shell


def calendar() -> rx.Component:
    return page_shell(
        page_heading(
            "Tournament Calendar",
            "Races, qualifiers, incentives, and community nights",
        ),
        rx.el.p(
            "Stay up to date with all Fresh Faces 4 activities. This calendar includes tournament races, qualifiers, incentives, community nights, and Q&A sessions.",
            class_name="ff-script-font mb-6 text-center text-sky-100/80",
        ),
        rx.el.div(
            rx.el.iframe(
                src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FDetroit&showPrint=0&src=cmFuZG80dWtyYWluZUBnbWFpbC5jb20&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t&color=%23039be5&color=%230b8043",
                width="100%",
                height="600",
                custom_attrs={"frameborder": "0", "scrolling": "no"},
                class_name="min-h-[28rem] w-full rounded-2xl border border-white/15 bg-slate-950",
            ),
            class_name="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.04] p-3 shadow-[0_0_40px_rgba(56,189,248,0.12)] backdrop-blur-md md:p-5",
        ),
    )
