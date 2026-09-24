"""Visit tracking state. Reads and writes the local SQLite file."""

import asyncio
import json
import os

import reflex as rx
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.visits import count_visitors, log_visit as save_visit

load_dotenv()

# Turn a URL path like "/about" into a short page name for the log.
_PAGE_NAMES = {
    "/": "home",
    "/about": "about",
    "/calendar": "calendar",
    "/credits": "credits",
    "/help": "help",
    "/tools": "tools",
}

# Google Form question that stores the player's division.
_DIVISION_QUESTION_ID = "3ff74616"
_FORMS_SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly"]


def _page_name(path: str) -> str:
    clean = (path or "/").rstrip("/") or "/"
    return _PAGE_NAMES.get(clean, clean.strip("/") or "home")


def _division_value(response: dict) -> str:
    """Read one RSVP's division, or "" if that answer is missing."""
    try:
        return response["answers"][_DIVISION_QUESTION_ID]["textAnswers"]["answers"][0]["value"]
    except (KeyError, IndexError, TypeError):
        return ""


def fetch_form_counts() -> dict[str, int]:
    """Download the RSVP form once and count responses plus each division."""
    raw_creds = os.getenv("SERVICE_ACCOUNT_JSON")
    form_id = os.getenv("RSVP_FORM_ID")

    if not raw_creds:
        raise RuntimeError("Missing SERVICE_ACCOUNT_JSON")
    if not form_id:
        raise RuntimeError("Missing RSVP_FORM_ID")

    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw_creds),
        scopes=_FORMS_SCOPES,
    )
    service = build("forms", "v1", credentials=creds)
    result = service.forms().responses().list(formId=form_id).execute()
    responses = result.get("responses", [])
    divisions = [_division_value(response) for response in responses]

    return {
        "rsvp_responses": len(responses),
        "fresh_faces": sum(value == "Fresh Faces" for value in divisions),
        "graduated_faces": sum(value == "Graduated Faces" for value in divisions),
        "veterans": sum(value == "Veterans" for value in divisions),
    }


class VisitState(rx.State):
    """Holds the visitor total shown on the home page."""

    total_visitors: int = 0
    present_views: int = int(os.getenv("PRESENT_VIEWS", "0"))
    rsvp_responses: int = 0
    fresh_faces: int = 0
    graduated_faces: int = 0
    veterans: int = 0

    @rx.var
    def visitor_count_label(self) -> str:
        # 1247 -> "1,247" so the poster number is easy to read
        return f"{self.total_visitors + self.present_views:,}"

    @rx.event
    def log_visit(self):
        """Save this page view, then refresh the form counts without blocking clicks."""
        path = self.router.url.path or self.router.route_id or "/"
        session_id = self.router.session.client_token or self.router.session.session_id
        save_visit(_page_name(path), session_id)
        self.total_visitors = count_visitors()
        return VisitState.load_form_counts

    @rx.event(background=True)
    async def load_form_counts(self):
        """Fetch RSVP totals off the UI thread, then write them onto state."""
        try:
            counts = await asyncio.to_thread(fetch_form_counts)
        except Exception as e:
            print("Error retrieving RSVP count:", e)
            return
        async with self:
            self.rsvp_responses = counts["rsvp_responses"]
            self.fresh_faces = counts["fresh_faces"]
            self.graduated_faces = counts["graduated_faces"]
            self.veterans = counts["veterans"]
