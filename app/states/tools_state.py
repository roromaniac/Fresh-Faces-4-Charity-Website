"""In-memory tools state. No Reflex database models."""

from typing import TypedDict

import requests
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
    uploaded_loadless_file: str = ""
    has_uploaded: bool = False

    @rx.event
    def reset_status(self):
        self.loadless_status = ""
        self.has_uploaded = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.loadless_status = ""
        self.has_uploaded = False

        if not files:
            self.loadless_status = "No file uploaded."
            return
        
        loadless_file = files[0]
        # Save uploaded file to disk
        upload_data = await loadless_file.read()
        outfile = rx.get_upload_dir() / loadless_file.filename
        with outfile.open("wb") as file_object:
            file_object.write(upload_data)
        
        self.uploaded_loadless_file = str(outfile)

        # Now compare with the official template
        reference_url = "https://github.com/aliosgaming/KH2FM_Load_Remover-FOR-RANDOMIZER/releases/latest/download/LiveSplit.KH2Randomizer.asl"
        try:
            response = requests.get(reference_url)
            response.raise_for_status()
            reference_text = response.text.strip()

            # Read the uploaded file as text (ignore errors)
            with open(outfile, "r", encoding="utf-8", errors="ignore") as uploaded_file:
                uploaded_text = uploaded_file.read().strip()

            self.has_uploaded = True

            # Actually compare the files: allow minor whitespace differences by stripping
            if uploaded_text == reference_text:
                self.loadless_status = "✅ Valid KH2 Randomizer loadless timer file! Your file matches the official template."
            else:
                # Optionally, be more sophisticated and compare ignoring line endings or excess empty lines
                from difflib import SequenceMatcher
                matcher = SequenceMatcher(None, uploaded_text, reference_text)
                similarity = matcher.ratio()
                if similarity > 0.98:
                    self.loadless_status = "✅ Your .asl file closely matches the official template (98%+ similar)."
                else:
                    self.loadless_status = (
                        "❌ Invalid KH2 Randomizer loadless timer file. Your file does not match the official template. "
                        "Please download the correct, most recent version using the link above."
                    )
        except FileNotFoundError:
            self.loadless_status = "❌ Reference file not found. Please ensure your file is valid and of .asl format."
        except Exception as e:
            self.loadless_status = f"❌ Error processing file: {str(e)}. Double check your file and try again."
