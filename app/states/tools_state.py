"""In-memory tools state. No Reflex database models."""

from typing import TypedDict

import reflex as rx


class PlayerRecord(TypedDict):
    discord_name: str
    twitch_name: str
    is_eligible: bool
    reason: str


class CheckboxState(rx.State):
    setup_tasks: list[str] = [
        "Install Kingdom Hearts 2 Final Mix",
        "Install the KH2 Randomizer (Panacea / OpenKH)",
        "Update the loadless timer to the latest rando release",
        "RSVP for Fresh Faces 4",
        "Join the tournament Discord and say hello",
    ]
    checked_tasks: dict[str, bool] = {}

    @rx.event
    def reset_checklist(self):
        self.checked_tasks = {task: False for task in self.setup_tasks}

    @rx.event
    def toggle_task(self, task: str, checked: bool):
        # Re-assign the whole dict so Reflex notices the change
        self.checked_tasks = {**self.checked_tasks, task: checked}


class LookUpState(rx.State):
    # Add known players here later. The lookup searches this list only.
    records: list[PlayerRecord] = []
    found_players: list[PlayerRecord] = []

    @rx.event
    def reset_records(self):
        self.found_players = []

    @rx.event
    def handle_submit(self, form_data: dict):
        query = str(form_data.get("input", "")).strip().lower()
        if not query:
            self.found_players = []
            return
        self.found_players = [
            player
            for player in self.records
            if query in player["discord_name"].lower()
            or query in player["twitch_name"].lower()
        ]


class LoadlessCheckerState(rx.State):
    loadless_status: str = ""

    @rx.event
    def reset_status(self):
        self.loadless_status = ""

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            self.loadless_status = "No file uploaded."
            return
        upload = files[0]
        name = upload.filename or "uploaded file"
        data = await upload.read()
        text = data.decode("utf-8", errors="ignore")
        looks_like_asl = name.lower().endswith(".asl") or "state" in text.lower()
        if looks_like_asl:
            self.loadless_status = (
                f"Received {name}. Compare it with the latest KH2FM Load Remover "
                "for Randomizer release to confirm you are up to date."
            )
        else:
            self.loadless_status = (
                f"Received {name}, but it does not look like a .asl timer file."
            )
