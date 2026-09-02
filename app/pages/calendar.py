import reflex as rx

from app.components.page_shell import page_heading, page_shell


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
                src=(
                    "https://calendar.google.com/calendar/embed"
                    "?height=900"
                    "&wkst=1"
                    "&ctz=America%2FDetroit"
                    "&showPrint=0"
                    "&src=cmFuZG80dWtyYWluZUBnbWFpbC5jb20"
                    "&src=ZW4udXNhI2hvbGlkYXlAZ3JvdXAudi5jYWxlbmRhci5nb29nbGUuY29t"
                    "&color=%23039be5&color=%230b8043"
                ),
                # Adjust the width to 1.5x the old reference (which was 95vw)
                width="142.5vw",  # 95vw * 1.5 = 142.5vw
                height="60vw",
                custom_attrs={"frameborder": "0", "scrolling": "no"},
                class_name=(
                    "rounded-2xl border border-white/15 bg-slate-950"
                ),
                style={
                    # Responsive, 1.5x as wide as before but still relative to the window!
                    "width": "142.5vw",
                    "height": "60vw",
                    "maxWidth": "150vw",      # allow up to 150vw as a "max width"
                    "maxHeight": "900px",
                    "minWidth": "480px",      # bump up minimum width for larger view
                    "minHeight": "350px",
                    "display": "block",
                    "marginLeft": "auto",
                    "marginRight": "auto",
                    "boxSizing": "border-box",
                },
            ),
            class_name=(
                "rounded-2xl border border-white/10 "
                "bg-white/[0.04] p-3 shadow-[0_0_40px_rgba(56,189,248,0.12)] "
                "backdrop-blur-md md:p-7 xl:p-12 flex justify-center"
            ),
            style={
                "width": "100%",
                "overflowX": "auto",
                "justifyContent": "center",
                "display": "flex",
            },
        ),
    )
