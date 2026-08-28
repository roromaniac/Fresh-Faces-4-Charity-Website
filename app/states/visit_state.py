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


class VisitState(rx.State):
    """Holds the visitor total shown on the home page."""

    total_visitors: int = 0

    @rx.var
    def visitor_count_label(self) -> str:
        # 1247 -> "1,247" so the poster number is easy to read
        return f"{self.total_visitors:,}"

    @rx.event
    def log_visit(self):
        """Run on every page load. Saves the visit, then refreshes the count."""
        path = self.router.url.path or self.router.route_id or "/"
        session_id = self.router.session.client_token or self.router.session.session_id
        save_visit(_page_name(path), session_id)
        self.total_visitors = count_visitors()
