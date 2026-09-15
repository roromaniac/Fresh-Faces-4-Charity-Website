"""Visit tracking state. Reads and writes the local SQLite file."""

import reflex as rx

from app.visits import count_visitors, log_visit as save_visit

# Turn a URL path like "/about" into a short page name for the log.
_PAGE_NAMES = {
    "/": "home",
    "/about": "about",
    "/calendar": "calendar",
    "/credits": "credits",
    "/help": "help",
    "/tools": "tools",
}


def _page_name(path: str) -> str:
    clean = (path or "/").rstrip("/") or "/"
    return _PAGE_NAMES.get(clean, clean.strip("/") or "home")


import os
import json
import asyncio
from datetime import datetime, timezone

from sqlmodel import select, func

from google.oauth2 import service_account
from googleapiclient.discovery import build

class VisitState(rx.State):
    """Holds the visitor total shown on the home page."""

    total_visitors: int = 0
    rsvp_responses: int = 0
    fresh_faces: int = 0
    graduated_faces: int = 0
    veterans: int = 0

    @rx.var
    def visitor_count_label(self) -> str:
        # 1247 -> "1,247" so the poster number is easy to read
        return f"{self.total_visitors:,}"

    @rx.event
    async def log_visit(self):
        """Run on every page load. Saves the visit, then refreshes the count."""
        path = self.router.url.path or self.router.route_id or "/"
        session_id = self.router.session.client_token or self.router.session.session_id
        save_visit(_page_name(path), session_id)
        self.total_visitors = count_visitors()
        try:
            # Run the blocking Google API call in a separate thread
            self.rsvp_responses = await asyncio.to_thread(self.get_rsvp_count)
            division_counts = await asyncio.to_thread(self.get_division_counts)
            self.fresh_faces = division_counts["fresh_faces"]
            self.graduated_faces = division_counts["graduated_faces"]
            self.veterans = division_counts["veterans"]
        except Exception as e:
            print("Error retrieving RSVP count:", e)

    def get_rsvp_count(self) -> int:
        SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly"]

        raw_creds = os.getenv("SERVICE_ACCOUNT_JSON")
        form_id = os.getenv("RSVP_FORM_ID")

        print("SERVICE_ACCOUNT_JSON present:", bool(raw_creds))
        print("RSVP_FORM_ID present:", bool(form_id))

        if not raw_creds:
            raise RuntimeError("Missing SERVICE_ACCOUNT_JSON")

        if not form_id:
            raise RuntimeError("Missing RSVP_FORM_ID")

        creds_info = json.loads(raw_creds)

        print("Service account project:", creds_info.get("project_id"))
        print("Service account email:", creds_info.get("client_email"))

        creds = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=SCOPES,
        )

        service = build("forms", "v1", credentials=creds)

        result = (
            service.forms()
            .responses()
            .list(formId=form_id)
            .execute()
        )

        print(result)

        return len(result.get("responses", []))

    def get_division_counts(self) -> dict[str, int]:

        SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly"]

        raw_creds = os.getenv("SERVICE_ACCOUNT_JSON")
        form_id = os.getenv("RSVP_FORM_ID")

        print("SERVICE_ACCOUNT_JSON present:", bool(raw_creds))
        print("RSVP_FORM_ID present:", bool(form_id))

        if not raw_creds:
            raise RuntimeError("Missing SERVICE_ACCOUNT_JSON")

        if not form_id:
            raise RuntimeError("Missing RSVP_FORM_ID")

        creds_info = json.loads(raw_creds)

        print("Service account project:", creds_info.get("project_id"))
        print("Service account email:", creds_info.get("client_email"))

        creds = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=SCOPES,
        )

        service = build("forms", "v1", credentials=creds)

        result = (
            service.forms()
            .responses()
            .list(formId=form_id)
            .execute()
        )

        try:
            responses = result.get("responses", [])
            fresh_faces_count = sum(([x["answers"]["3ff74616"]["textAnswers"]["answers"][0]["value"] == "Fresh Faces" for x in responses]))
            graduated_faces_count = sum(([x["answers"]["3ff74616"]["textAnswers"]["answers"][0]["value"] == "Graduated Faces" for x in responses]))
            veterans_count = sum(([x["answers"]["3ff74616"]["textAnswers"]["answers"][0]["value"] == "Veterans" for x in responses]))
        except KeyError as e:
            print("There is a key error for calculating division counts:", e)
        except Exception as e:
            print("Error retrieving division counts:", e)
            return {"fresh_faces": 0, "graduated_faces": 0, "veterans": 0}

        return {"fresh_faces": fresh_faces_count, "graduated_faces": graduated_faces_count, "veterans": veterans_count}


 
