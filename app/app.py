import reflex as rx

from app.components.navbar import navbar
from app.components.poster import poster
from app.components.stream_bar import stream_bar


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        stream_bar(),
        poster(),
        class_name="ff-body flex h-dvh w-full flex-col overflow-hidden bg-slate-950",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/poster.css"],
    head_components=[
        rx.el.link(
            rel="preload",
            href="/KHTitle.woff2",
            as_="font",
            type="font/woff2",
            cross_origin="anonymous",
        ),
        rx.el.link(
            rel="preload",
            href="/KHMenu.woff2",
            as_="font",
            type="font/woff2",
            cross_origin="anonymous",
        ),
        rx.el.link(
            rel="preload",
            href="/KHMenuBold.woff2",
            as_="font",
            type="font/woff2",
            cross_origin="anonymous",
        ),
        rx.el.link(
            rel="preload",
            href="/KHData.woff2",
            as_="font",
            type="font/woff2",
            cross_origin="anonymous",
        ),
    ],
)
app.add_page(
    index, route="/", title="Fresh Faces 4 · Charity Showcase for Ukraine"
)
