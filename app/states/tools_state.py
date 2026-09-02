"""In-memory tools state. No Reflex database models."""

from typing import TypedDict

import sqlite3
import requests
import reflex as rx


class PlayerRecord(TypedDict):
    discord_name: str
    twitch_name: str
    is_eligible: bool
    reason: str


class CheckboxState(rx.State):
    setup_tasks: list[str] = [
        "Download KH2Tracker",
        "Download KH2Randomizer Generator",
        "Download Livesplit",
        "Ensure KH2 RANDO (not speedrun) Loadless Timer is Installed AND Functional",
        "Install OpenKH Mods Manager",
        "Install KH2FM-Mods-Num/GoA-ROM-Edition in Mods Manager",
        "Install KH2FM-Mods-equations19/auto-save in Mods Manager",
        "Install KH2FM-Mods-equations19/soft-reset in Mods Manager",
        "Install KH2FM-Mods-equations19/KH2-Lua-Library in Mods Manager",
        "Make racetime.gg Account",
        "Link Twitch to racetime.gg",
        "Test Setup by Playing a KH2 Rando Seed",
        "RSVP to Fresh Faces 3",
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
    fuzzy_search_dist: int = 2
    found_players: list[dict] = []

    def levenshtein(self, player_property: str, search_str: str) -> int:
        """Calculate simple Levenshtein distance for fuzzy search."""
        if player_property == search_str:
            return 0
        if not player_property or not search_str:
            return self.fuzzy_search_dist + 1

        prev = list(range(len(search_str) + 1))
        for i, c1 in enumerate(player_property):
            curr = [i + 1]
            for j, c2 in enumerate(search_str):
                insert = prev[j + 1] + 1
                delete = curr[j] + 1
                substitute = prev[j] + (c1 != c2)
                curr.append(min(insert, delete, substitute))
            prev = curr
        return prev[-1]

    @rx.event
    def reset_records(self):
        self.found_players = []

    @rx.event
    def handle_submit(self, form_data: dict):
        """
        Performs a fuzzy search and returns the eligibility for any player
        based on Discord Name, Twitch Name, or Player (case-insensitive).
        """
        search_text = str(form_data.get("input", "")).strip()
        if not search_text:
            self.found_players = []
            return

        search_text_lower = search_text.lower()
        conn = sqlite3.connect("data/eligibility.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                [Player],
                [Discord Name],
                [Twitch Name],
                [FF1 Placing],
                [FF2 Placing],
                [BB1 Placing],
                [FF3 Placing],
                [BB2 Placing],
                [eligible],
                [reason]
            FROM "FF4 Eligibility"
            """
        )
        past_players = cursor.fetchall()
        result_list = []

        for row in past_players:
            player, discord, twitch, ff1, ff2, bb1, ff3, bb2, eligible, reason = row
            player_names = [
                str(player or "").lower(),
                str(discord or "").lower(),
                str(twitch or "").lower()
            ]

            # Choose 'reason' and eligibility: e.g., eligible for FF3 if placing empty or as per a criterion.
            # Modify below as needed for your eligibility logic.
            # For example, let's check if 'FF3 Placing' is empty -> eligible.
            is_eligible = eligible == "Yes"
            reason = reason or "Not eligible."

            # Fuzzy/full/prefix search logic.
            full_match = any(name == search_text_lower and search_text_lower != "" for name in player_names)
            starts_with = any(name.startswith(search_text_lower) and search_text_lower != "" for name in player_names)
            distances = [
                self.levenshtein(str(player or ""), search_text),
                self.levenshtein(str(discord or ""), search_text),
                self.levenshtein(str(twitch or ""), search_text)
            ]
            best_distance = min(distances)

            # Prioritize: full match (rank 0), fuzzy match (rank = best_distance), prefix (rank = max_fuzzy + 1)
            score = None
            if full_match:
                score = 0
            elif best_distance <= self.fuzzy_search_dist:
                score = best_distance
            elif starts_with:
                score = self.fuzzy_search_dist + 1

            if score is not None:
                result_list.append((
                    score,
                    {
                        "is_eligible": is_eligible,
                        "discord_name": discord or player or "",
                        "twitch_name": twitch or "",
                        "reason": reason
                    }
                ))

        conn.close()
        # Sort by score (best matches first)
        result_list.sort(key=lambda x: x[0])
        # Only keep the player records
        self.found_players = [rec for _, rec in result_list]

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
