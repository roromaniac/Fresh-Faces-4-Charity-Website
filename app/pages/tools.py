import reflex as rx

from app.components.page_shell import page_heading, page_shell
from app.states.tools_state import CheckboxState, LoadlessCheckerState, LookUpState

_TIPS = [
    ("KH2 Rando Setup Video Guide (2025)", "https://www.youtube.com/watch?v=dsrk7hUPDxQ"),
    ("About KH2 Rando", "https://www.youtube.com/watch?v=AntmkVM0r4s"),
    ("KH2 Rando Shotgunning Tutorial", "https://www.youtube.com/watch?v=7ulNJkPhVSU"),
    ("Final Xemnas Dome Skip", "https://www.youtube.com/watch?v=3V7Tm7aJjCw"),
    ("The Experiment Tutorial", "https://www.youtube.com/watch?v=jLhjnnODdfk"),
    ("Groundshaker 1 Cycle", "https://youtube.com/shorts/ihIlkkGlFmQ?feature=share"),
    ("Thresholder 1 Cycle", "https://www.youtube.com/shorts/2_CT3K66CoA"),
    ("KH2 Rando Abilities for Beginners", "https://youtu.be/d4gr0Q9DLQE"),
    (
        "Abilities, Forms, and Summons Guide",
        "https://docs.google.com/document/d/1ULlWM8BQLk1J3ITsGwpJgffJcWwmq0EjFLvuQE0BLG8/edit?usp=sharing",
    ),
]


def tool_card(title: str, description: str, content: rx.Component) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.icon("crown", class_name="h-4 w-4 text-amber-200"),
            rx.el.h2(
                title,
                class_name="ff-menu-bold-font text-lg uppercase tracking-[0.08em] text-white",
            ),
            class_name="flex items-center gap-2 border-b border-white/10 bg-gradient-to-r from-sky-900/80 via-indigo-900/70 to-amber-900/40 px-5 py-3",
        ),
        rx.el.p(
            description,
            class_name="ff-menu-font px-5 pt-4 text-sm text-sky-100/80",
        ),
        rx.el.div(content, class_name="p-5"),
        class_name="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.04] shadow-[0_0_30px_rgba(56,189,248,0.10)] backdrop-blur-md",
    )


def _checklist() -> rx.Component:
    return rx.el.div(
        tool_card(
            "Task Checklist",
            "Need to know if you're ready to play in Fresh Faces 4? Use this checklist to confirm your setup steps.",
            rx.el.div(
                rx.foreach(
                    CheckboxState.setup_tasks,
                    lambda task: rx.el.div(
                        rx.checkbox(
                            checked=CheckboxState.checked_tasks.get(task, False),
                            on_change=lambda checked: CheckboxState.toggle_task(
                                task, checked
                            ),
                        ),
                        rx.el.span(task, class_name="flex-1 text-sky-50"),
                        rx.cond(
                            CheckboxState.checked_tasks.get(task, False),
                            rx.el.span(
                                "Completed",
                                class_name="ff-data-font text-xs uppercase tracking-[0.14em] text-emerald-300",
                            ),
                            rx.el.span(
                                "Incomplete",
                                class_name="ff-data-font text-xs uppercase tracking-[0.14em] text-rose-300",
                            ),
                        ),
                        class_name="flex items-center gap-3 rounded-xl border border-white/10 bg-slate-950/40 px-3 py-2",
                    ),
                ),
                class_name="flex flex-col gap-3",
            ),
        ),
        id="ff4-checklist",
    )


def _lookup() -> rx.Component:
    return rx.el.div(
        tool_card(
            "FF4 Eligibility Lookup",
            "Search a Discord ID or Twitch username to check Fresh Faces 4 eligibility. Contact roro on Discord for corrections.",
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            name="input",
                            placeholder="Discord ID or Twitch username",
                            type="text",
                            required=True,
                            class_name="w-full rounded-lg border border-white/15 bg-white px-3 py-2 text-slate-900",
                        ),
                        rx.el.button(
                            "Search",
                            type="submit",
                            class_name="rounded-lg bg-gradient-to-r from-sky-500 to-amber-400 px-5 py-2 font-semibold text-slate-950",
                        ),
                        class_name="flex flex-col gap-3 sm:flex-row",
                    ),
                    on_submit=LookUpState.handle_submit,
                    reset_on_submit=True,
                ),
                rx.el.h3(
                    "Results",
                    class_name="ff-menu-bold-font mt-6 text-lg text-white",
                ),
                rx.cond(
                    LookUpState.found_players.length() == 0,
                    rx.el.p(
                        "No results found.",
                        class_name="ff-menu-font mt-3 text-sky-200/70",
                    ),
                    rx.el.div(
                        rx.foreach(
                            LookUpState.found_players,
                            lambda player: rx.el.div(
                                rx.el.p(
                                    player["discord_name"],
                                    class_name="ff-menu-bold-font text-white",
                                ),
                                rx.el.p(
                                    player["twitch_name"],
                                    class_name="text-sm text-sky-100/80",
                                ),
                                rx.el.p(
                                    player["reason"],
                                    class_name="mt-2 text-sm text-amber-100/90",
                                ),
                                class_name="rounded-xl border border-white/10 bg-slate-950/40 p-4",
                            ),
                        ),
                        class_name="mt-3 flex flex-col gap-3",
                    ),
                ),
                class_name="flex flex-col",
            ),
        ),
        id="ff4-eligibility-lookup",
    )


def _loadless() -> rx.Component:
    return rx.el.div(
        tool_card(
            "Loadless Timer Validator",
            "Upload your .asl file to confirm you have a loadless timer ready for KH2 rando.",
            rx.el.div(
                rx.upload(
                    rx.el.p(
                        "Drop a .asl file here or click to upload.",
                        class_name="text-sky-100/80",
                    ),
                    id="upload",
                    max_files=1,
                    accept={"application/octet-stream": [".asl"]},
                    on_drop=LoadlessCheckerState.handle_upload(
                        rx.upload_files(upload_id="upload")
                    ),
                    class_name="flex min-h-32 w-full items-center justify-center rounded-xl border-2 border-dashed border-sky-300/40 bg-slate-950/40 p-6",
                ),
                rx.el.button(
                    "Clear last result",
                    on_click=LoadlessCheckerState.reset_status,
                    class_name="mt-4 rounded-lg border border-white/15 px-4 py-2 text-sm text-sky-100 hover:bg-white/10",
                ),
                rx.el.p(
                    LoadlessCheckerState.loadless_status,
                    class_name="mt-4 text-sky-100",
                ),
                class_name="flex flex-col items-center",
            ),
        ),
        id="ff4-loadless-checker",
    )


def _tips() -> rx.Component:
    return rx.el.div(
        tool_card(
            "KH2 Rando Tips and Tricks",
            "Tutorials and clips of common KH2 rando speedups for your Fresh Faces 4 races.",
            rx.el.ul(
                *[
                    rx.el.li(
                        rx.el.a(
                            title,
                            href=url,
                            target="_blank",
                            class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                        ),
                        class_name="mb-2",
                    )
                    for title, url in _TIPS
                ],
                class_name="grid list-disc gap-1 pl-5 sm:grid-cols-2 lg:grid-cols-3",
            ),
        ),
        id="ff4-tricks",
    )


def tools() -> rx.Component:
    return page_shell(
        page_heading(
            "Tools",
            "Prep the keyblade, then join the night",
        ),
        rx.el.div(
            _checklist(),
            _lookup(),
            _loadless(),
            _tips(),
            class_name="flex flex-col gap-6",
        ),
    )
