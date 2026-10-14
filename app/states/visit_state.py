"""Visit tracking state. Reads and writes the local SQLite file."""

import asyncio
import json
import os
import threading

import reflex as rx
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.visits import record_page_view

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

# One shared RSVP tally. The startup loop refreshes it; page loads only read it.
_form_lock = threading.Lock()
_form_ready = threading.Event()
_form_service = None
_form_counts = {
    "rsvp_responses": 0,
    "fresh_faces": 0,
    "graduated_faces": 0,
    "veterans": 0,
}


def _page_name(path: str) -> str:
    clean = (path or "/").rstrip("/") or "/"
    return _PAGE_NAMES.get(clean, clean.strip("/") or "home")


def _division_value(response: dict) -> str:
    """Read one RSVP's division, or "" if that answer is missing."""
    try:
        return response["answers"][_DIVISION_QUESTION_ID]["textAnswers"]["answers"][0]["value"]
    except (KeyError, IndexError, TypeError):
        return ""


def _forms_service():
    """Build the Google Forms client once and reuse it for later downloads."""
    global _form_service
    if _form_service is not None:
        return _form_service

    raw_creds = os.getenv("SERVICE_ACCOUNT_JSON")
    if not raw_creds:
        raise RuntimeError("Missing SERVICE_ACCOUNT_JSON")

    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw_creds),
        scopes=_FORMS_SCOPES,
    )
    _form_service = build("forms", "v1", credentials=creds)
    return _form_service


def fetch_form_counts() -> dict[str, int]:
    """Download the RSVP form once and count responses plus each division."""
    form_id = os.getenv("RSVP_FORM_ID")
    if not form_id:
        raise RuntimeError("Missing RSVP_FORM_ID")

    service = _forms_service()
    result = service.forms().responses().list(formId=form_id).execute()
    responses = result.get("responses", [])
    divisions = [_division_value(response) for response in responses]

    return {
        "rsvp_responses": len(responses),
        "fresh_faces": sum(value == "Fresh Faces" for value in divisions),
        "graduated_faces": sum(value == "Graduated Faces" for value in divisions),
        "veterans": sum(value == "Veterans" for value in divisions),
    }


def cached_form_counts() -> dict[str, int]:
    """Return the last saved RSVP totals. This does not call Google."""
    with _form_lock:
        return dict(_form_counts)


def refresh_form_counts() -> dict[str, int]:
    """Download the RSVP form and save the totals for every visitor to share."""
    try:
        counts = fetch_form_counts()
    except Exception:
        # Let a page that is waiting on the first download move on.
        _form_ready.set()
        raise
    with _form_lock:
        _form_counts.update(counts)
    _form_ready.set()
    return dict(counts)


def wait_for_form_counts(timeout: float = 30) -> dict[str, int]:
    """Wait until the shared download finishes, then return the saved totals."""
    _form_ready.wait(timeout)
    return cached_form_counts()


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

    @rx.event(background=True)
    async def log_visit(self):
        """Save this page view, then copy the shared visitor and RSVP totals."""
        # Copy the page and session while the lock is held. The database work stays outside it.
        async with self:
            path = self.router.url.path or self.router.route_id or "/"
            session_id = self.router.session.client_token or self.router.session.session_id
        page = _page_name(path)
        total = None
        try:
            total = await asyncio.to_thread(
                record_page_view,
                page,
                str(session_id or ""),
            )
        except Exception as e:
            print("Error saving visit:", e)

        # Division counts are only shown on the home page. Read the saved copy.
        # The first home visit after startup waits for the one shared download.
        counts = None
        if page == "home":
            try:
                if _form_ready.is_set():
                    counts = cached_form_counts()
                else:
                    counts = await asyncio.to_thread(wait_for_form_counts)
            except Exception as e:
                print("Error retrieving RSVP count:", e)

        async with self:
            if total is not None:
                self.total_visitors = total
            if counts is not None:
                self.rsvp_responses = counts["rsvp_responses"]
                self.fresh_faces = counts["fresh_faces"]
                self.graduated_faces = counts["graduated_faces"]
                self.veterans = counts["veterans"]
