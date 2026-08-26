import reflex as rx

TWITCH_PATH = "M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714z"

YOUTUBE_PATH = "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"


def _brand_svg(path: str, class_name: str) -> rx.Component:
    return rx.el.svg(
        rx.el.svg.path(d=path),
        view_box="0 0 24 24",
        fill="currentColor",
        xmlns="http://www.w3.org/2000/svg",
        aria_hidden="true",
        class_name=class_name,
    )


def twitch_glyph(
    class_name: str = "h-3.5 w-3.5 text-[#efe7ff]",
) -> rx.Component:
    return _brand_svg(TWITCH_PATH, class_name)


def youtube_glyph(class_name: str = "h-3.5 w-3.5 text-white") -> rx.Component:
    return _brand_svg(YOUTUBE_PATH, class_name)
