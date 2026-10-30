import asyncio

import reflex as rx
from reflex.app import EventNamespace

# --- Deployment fix ---------------------------------------------------------
# On the server, the browser sends an extra "auth" value when it connects to
# the websocket. Reflex's on_connect only accepts (sid, environ), so it crashed
# with "takes 3 positional arguments but 4 were given" and the page never
# became interactive. We wrap it so it quietly accepts (and ignores) "auth".
_original_on_connect = EventNamespace.on_connect


async def _on_connect_accepting_auth(self, sid, environ, auth=None):
    return await _original_on_connect(self, sid, environ)


EventNamespace.on_connect = _on_connect_accepting_auth
# ----------------------------------------------------------------------------

from app.components.navbar import navbar
from app.components.poster import poster
from app.components.stream_bar import stream_bar

from app.pages.about import about
from app.pages.calendar import calendar
from app.pages.credits import credits
from app.pages.help import help_page
from app.pages.tools import tools
from app.pages.window_overlay import left_window_high_res, right_window_high_res
from app.states.tools_state import (
    CheckboxState,
    LoadlessCheckerState,
    LookUpState,
)
from app.states.visit_state import VisitState, refresh_form_counts
from app.visits import resync_visitor_total

from app.scripts.check_live_streams import refresh_live_cache
from app.scripts.eligibility import main as eligibility_main
from app.states.stream_state import STREAM_LINKS

async def initialize_eligibility():
    # Rebuild the eligibility database off the event loop so page clicks stay live.
    await asyncio.to_thread(eligibility_main)

async def poll_live_streams():
    """Ask Twitch and YouTube once a minute for every visitor to share."""
    while True:
        try:
            await asyncio.to_thread(refresh_live_cache, STREAM_LINKS)
        except Exception as exc:
            print("Live check failed:", exc)
        await asyncio.sleep(60)

# How many seconds to wait between checks.
POLL_SECONDS = 15
# Every Nth check is a full recount, which also catches deleted RSVPs.
# 40 checks x 15 seconds = a full recount about every 10 minutes.
FULL_RECOUNT_EVERY = 40

async def poll_form_counts():
    """Update RSVP and visit totals every 15 seconds for every visitor to share."""
    run = 0
    while True:
        # The very first run (run 0) is also full, to fix any drift from downtime.
        full = run % FULL_RECOUNT_EVERY == 0
        try:
            # to_thread keeps the slow Google call off the main loop.
            await asyncio.to_thread(refresh_form_counts, full)
        except Exception as exc:
            print("RSVP count failed:", exc)
        try:
            # Re-check the visit total against the database every run so
            # a missed save is corrected within about 15 seconds.
            await asyncio.to_thread(resync_visitor_total)
        except Exception as exc:
            print("Visit recount failed:", exc)
        run += 1
        await asyncio.sleep(POLL_SECONDS)

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
    # watch_counts keeps the numbers live while the page stays open.
    on_load=[VisitState.log_visit, VisitState.watch_counts],
)
app.add_page(
    about,
    route="/about",
    title="About Fresh Faces 4",
    on_load=VisitState.log_visit,
)
app.add_page(
    calendar,
    route="/calendar",
    title="Calendar",
    on_load=VisitState.log_visit,
)
app.add_page(
    credits,
    route="/credits",
    title="Credits",
    on_load=VisitState.log_visit,
)
app.add_page(
    help_page,
    route="/help",
    title="Help",
    on_load=VisitState.log_visit,
)
app.add_page(
    tools,
    route="/tools",
    title="Tools",
    on_load=[
        VisitState.log_visit,
        CheckboxState.reset_checklist,
        LoadlessCheckerState.reset_status,
        LookUpState.reset_records,
    ],
)

app.add_page(
    left_window_high_res,
    route="/left-window-high-res",
    title="Left Window",
)
app.add_page(
    right_window_high_res,
    route="/right-window-high-res",
    title="Right Window",
)

app.register_lifespan_task(initialize_eligibility)
app.register_lifespan_task(poll_live_streams)
app.register_lifespan_task(poll_form_counts)