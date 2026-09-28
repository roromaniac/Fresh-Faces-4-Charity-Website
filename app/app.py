import asyncio

import reflex as rx

from app.components.navbar import navbar
from app.components.poster import poster
from app.components.stream_bar import stream_bar

from app.pages.about import about
from app.pages.calendar import calendar
from app.pages.credits import credits
from app.pages.help import help_page
from app.pages.tools import tools
from app.states.nav_state import NavState
from app.states.tools_state import (
    CheckboxState,
    LoadlessCheckerState,
    LookUpState,
)
from app.states.visit_state import VisitState

from app.scripts.check_live_streams import refresh_live_cache
from app.scripts.eligibility import main as eligibility_main
from app.states.stream_state import STREAM_LINKS
from app.visits import init_db

async def initialize_eligibility():
    # Rebuild the eligibility database off the event loop so page clicks stay live.
    await asyncio.to_thread(eligibility_main)

async def initialize_visits():
    # Create the visits table once, instead of on every page view.
    await asyncio.to_thread(init_db)

async def poll_live_streams():
    """Ask Twitch and YouTube once a minute for every visitor to share."""
    while True:
        try:
            await asyncio.to_thread(refresh_live_cache, STREAM_LINKS)
        except Exception as exc:
            print("Live check failed:", exc)
        await asyncio.sleep(60)

def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        stream_bar(),
        poster(),
        class_name="ff-body flex h-dvh w-full flex-col overflow-hidden bg-slate-950",
    )

app = rx.App(
    # theme=rx.theme(appearance="light"),
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
    index,
    route="/",
    title="Fresh Faces 4",
    on_load=[VisitState.log_visit, NavState.mark_active("/")],
)
app.add_page(
    about,
    route="/about",
    title="About Fresh Faces 4",
    on_load=[VisitState.log_visit, NavState.mark_active("/about")],
)
app.add_page(
    calendar,
    route="/calendar",
    title="Calendar",
    on_load=[VisitState.log_visit, NavState.mark_active("/calendar")],
)
app.add_page(
    credits,
    route="/credits",
    title="Credits",
    on_load=[VisitState.log_visit, NavState.mark_active("/credits")],
)
app.add_page(
    help_page,
    route="/help",
    title="Help",
    on_load=[VisitState.log_visit, NavState.mark_active("/help")],
)
app.add_page(
    tools,
    route="/tools",
    title="Tools",
    on_load=[
        VisitState.log_visit,
        NavState.mark_active("/tools"),
        CheckboxState.reset_checklist,
        LoadlessCheckerState.reset_status,
        LookUpState.reset_records,
    ],
)

app.register_lifespan_task(initialize_eligibility)
app.register_lifespan_task(initialize_visits)
app.register_lifespan_task(poll_live_streams)