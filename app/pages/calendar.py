import reflex as rx

from app.components.page_shell import page_heading, page_shell

# Google uses the visitor's local timezone when `ctz` is omitted.
CALENDAR_BASE_URL = (
    "https://calendar.google.com/calendar/embed"
    "?height=600"
    "&wkst=1"
    "&showPrint=0"
    "&src=cmFuZG80dWtyYWluZUBnbWFpbC5jb20"
    "&src=YTY3NTc1MTJhMDU4NWViNGMwYjFmMDFiNDAxYjUwNGFhNTkyYjA0NTViMzM1OWQzZTNhYTA0OWUzMjVkNDIwOUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t"
    "&src=NGViMTg4ZGVlNjE4Y2E5OGFlY2IyNGRmMjdiZTU0NWEwZjU2OWViMWQ0MTIyOTM0Y2M1ZWVkNjQzYzBhMjc2M0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t"
    "&color=%23039be5&color=%230b8043&color=%23f4511e"
)


def calendar() -> rx.Component:
    return page_shell(
        page_heading(
            "Tournament Calendar",
            "The Full Calendar of Upcoming Events for Fresh Faces 4",
        ),
        rx.el.p(
            "Stay up to date with all Fresh Faces 4 activities. This calendar includes tournament races, qualifiers, incentives, community nights, and Q&A sessions.",
            class_name="ff-menu-font mb-6 text-center text-sky-100/80",
        ),
        rx.el.div(
            rx.el.iframe(
                src=CALENDAR_BASE_URL,
                title="Fresh Faces 4 event calendar",
                custom_attrs={"frameborder": "0", "scrolling": "no"},
                class_name=(
                    "h-[70vh] min-h-[350px] w-full rounded-2xl "
                    "border border-white/15 bg-slate-950"
                ),
            ),
            class_name=(
                "rounded-2xl border border-white/10 "
                "bg-white/[0.04] p-3 shadow-[0_0_40px_rgba(56,189,248,0.12)] "
                "backdrop-blur-md md:p-7"
            ),
        ),
    )
