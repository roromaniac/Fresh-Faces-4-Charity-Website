"""Visit tracking state. Reads and writes the local SQLite file."""

import asyncio
import json
import os
import threading

import reflex as rx
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.visits import (
    DB_PATH,
    cached_visitor_total,
    remember_visitor,
    save_page_view,
)

load_dotenv()


def _saved_views() -> int:
    """Visits from before this database existed. Read on each page view.

    The number lives in PRESENT_VIEWS. Reading it here, instead of trusting a
    saved copy, keeps old browser sessions from dropping the baseline.
    """
    raw = os.getenv("PRESENT_VIEWS", "0") or "0"
    try:
        return max(int(raw), 0)
    except ValueError:
        return 0


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
_DIVISION_FIELDS = {
    "Fresh Faces": "fresh_faces",
    "Graduated Faces": "graduated_faces",
    "Veterans": "veterans",
}
_FORMS_SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly"]

# Saved RSVP totals. Page loads read this file's numbers while Google catches up.
_FORM_CACHE_PATH = DB_PATH.parent / "form_counts.json"

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
# Ids we already counted, and the newest RSVP time we have asked Google for.
_seen_response_ids: set[str] = set()
_newest_response_time = ""


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


def _download_responses(since: str) -> list[dict]:
    """Download RSVPs. After the first time, only RSVPs newer than `since`."""
    form_id = os.getenv("RSVP_FORM_ID")
    if not form_id:
        raise RuntimeError("Missing RSVP_FORM_ID")

    service = _forms_service()
    found: list[dict] = []
    page_token = ""
    # Google returns at most 5000 RSVPs per page.
    for _ in range(20):
        options: dict = {"formId": form_id, "pageSize": 5000}
        if page_token:
            options["pageToken"] = page_token
        if since:
            options["filter"] = f"timestamp > {since}"
        result = service.forms().responses().list(**options).execute()
        found.extend(result.get("responses", []))
        page_token = result.get("nextPageToken") or ""
        if not page_token:
            break
    return found


def _note_response(response: dict) -> bool:
    """Add one RSVP to the saved totals. Caller must hold _form_lock.

    Returns True when this RSVP was not counted before.
    """
    global _newest_response_time
    response_id = str(response.get("responseId") or "")
    submitted = str(response.get("lastSubmittedTime") or response.get("createTime") or "")
    if submitted > _newest_response_time:
        _newest_response_time = submitted
    if not response_id or response_id in _seen_response_ids:
        return False

    _seen_response_ids.add(response_id)
    _form_counts["rsvp_responses"] += 1
    field = _DIVISION_FIELDS.get(_division_value(response))
    if field:
        _form_counts[field] += 1
    return True


def _load_saved_counts() -> None:
    """Put the last saved RSVP totals in memory so the first page is not blank."""
    global _newest_response_time
    if not _FORM_CACHE_PATH.exists():
        return
    try:
        saved = json.loads(_FORM_CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return
    seen = saved.get("seen")
    since = str(saved.get("since") or "")
    # Without the timestamp we would download every RSVP and count them twice.
    if not since or not isinstance(seen, list):
        return

    with _form_lock:
        for key in _form_counts:
            try:
                _form_counts[key] = int(saved.get(key, 0))
            except (TypeError, ValueError):
                _form_counts[key] = 0
        _seen_response_ids.clear()
        _seen_response_ids.update(str(item) for item in seen)
        _newest_response_time = since
    _form_ready.set()


def _write_form_cache(snapshot: dict) -> None:
    """Save the RSVP totals so the next startup can show them immediately."""
    _FORM_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = _FORM_CACHE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(snapshot), encoding="utf-8")
    temporary.replace(_FORM_CACHE_PATH)


def cached_form_counts() -> dict[str, int]:
    """Return the last saved RSVP totals. This does not call Google."""
    with _form_lock:
        return dict(_form_counts)


def refresh_form_counts() -> dict[str, int]:
    """Download new RSVPs and add them to the totals every visitor shares."""
    with _form_lock:
        since = _newest_response_time
    try:
        responses = _download_responses(since)
    except Exception:
        # Let a page that is waiting on the first download move on.
        _form_ready.set()
        raise

    changed = False
    with _form_lock:
        for response in responses:
            if _note_response(response):
                changed = True
        counts = dict(_form_counts)
        snapshot = {
            "rsvp_responses": counts["rsvp_responses"],
            "fresh_faces": counts["fresh_faces"],
            "graduated_faces": counts["graduated_faces"],
            "veterans": counts["veterans"],
            "since": _newest_response_time,
            "seen": list(_seen_response_ids),
        }
    _form_ready.set()
    if snapshot["since"] and (changed or not _FORM_CACHE_PATH.exists()):
        try:
            _write_form_cache(snapshot)
        except OSError as exc:
            print("Error saving RSVP count:", exc)
    return counts


def wait_for_form_counts(timeout: float = 30) -> dict[str, int]:
    """Wait until the shared download finishes, then return the saved totals."""
    _form_ready.wait(timeout)
    return cached_form_counts()


_load_saved_counts()


# Do not open SQLite while the backend is importing. Reflex Cloud must finish
# starting before optional visit logging touches disk.
_BOOT_VISITORS = 0
_BOOT_COUNTS = cached_form_counts()


class VisitState(rx.State):
    """Holds the visitor total shown on the home page."""

    total_visitors: int = _BOOT_VISITORS
    present_views: int = _saved_views()
    rsvp_responses: int = _BOOT_COUNTS["rsvp_responses"]
    fresh_faces: int = _BOOT_COUNTS["fresh_faces"]
    graduated_faces: int = _BOOT_COUNTS["graduated_faces"]
    veterans: int = _BOOT_COUNTS["veterans"]

    @rx.var
    def visitor_count_label(self) -> str:
        # 1247 -> "1,247" so the poster number is easy to read
        return f"{self.total_visitors + self.present_views:,}"

    def _show_counts(self, counts: dict[str, int]) -> None:
        """Copy RSVP totals onto the page. Call this while holding the state."""
        self.rsvp_responses = counts["rsvp_responses"]
        self.fresh_faces = counts["fresh_faces"]
        self.graduated_faces = counts["graduated_faces"]
        self.veterans = counts["veterans"]

    @rx.event(background=True)
    async def log_visit(self):
        """Show the last totals right away, then save this visit."""
        # Copy the page and session while the lock is held.
        async with self:
            path = self.router.url.path or self.router.route_id or "/"
            session_id = str(
                self.router.session.client_token or self.router.session.session_id or ""
            )
        page = _page_name(path)

        # Previous numbers go on screen before any slow disk or Google work.
        previous_total = cached_visitor_total()
        counts = cached_form_counts() if page == "home" and _form_ready.is_set() else None
        async with self:
            # Refresh the baseline every time. A saved session may still have 0.
            self.present_views = _saved_views()
            if previous_total is not None:
                self.total_visitors = previous_total
            if counts is not None:
                self._show_counts(counts)

        total = None
        try:
            total = await asyncio.to_thread(remember_visitor, session_id)
        except Exception as e:
            print("Error counting visit:", e)

        if total is not None:
            async with self:
                self.present_views = _saved_views()
                if self.total_visitors != total:
                    self.total_visitors = total

        try:
            await asyncio.to_thread(save_page_view, page, session_id)
        except Exception as e:
            print("Error saving visit:", e)

        # Cold start has no saved RSVP totals yet. Keep showing the old
        # numbers, then fill in the real ones when Google answers.
        if page == "home" and not _form_ready.is_set():
            try:
                counts = await asyncio.to_thread(wait_for_form_counts)
            except Exception as e:
                print("Error retrieving RSVP count:", e)
                counts = None
            if counts is not None:
                async with self:
                    self._show_counts(counts)
