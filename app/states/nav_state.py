from typing import TypedDict

import reflex as rx


class NavLink(TypedDict):
    label: str
    href: str
    icon: str


class NavState(rx.State):
    mobile_open: bool = False
    links: list[NavLink] = [
        {"label": "Home", "href": "/", "icon": "house"},
        {"label": "About", "href": "/about", "icon": "heart"},
        {"label": "Calendar", "href": "/calendar", "icon": "calendar-heart"},
        {"label": "Tools", "href": "/tools", "icon": "key-round"},
        {"label": "Help", "href": "/help", "icon": "circle-help"},
        {"label": "Credits", "href": "/credits", "icon": "crown"},
    ]

    @rx.var
    def active_href(self) -> str:
        """Highlight the link for the page that is actually open."""
        path = (self.router.url.path or "/").rstrip("/")
        return path or "/"

    @rx.event
    def toggle_menu(self):
        self.mobile_open = not self.mobile_open

    @rx.event
    def close_menu(self):
        self.mobile_open = False

    @rx.event
    def select_link(self, href: str):
        self.mobile_open = False
        return rx.redirect(href)
