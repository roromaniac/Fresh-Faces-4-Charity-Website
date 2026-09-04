from typing import TypedDict

import reflex as rx


class Partner(TypedDict):
    name: str
    image: str


class Stat(TypedDict):
    value: str
    label: str


class EventState(rx.State):
    event_name: str = "Fresh Faces 4"
    logo_image: str = "/kh2rando.png"
    logo_icon: str = "heart"
    tagline: str = "A KH2 Rando Charity Production for Project Hope (Ukraine)"
    date_line: str = "Saturday, June 14 · 5:00 PM"
    venue_line: str = "The Lumen Hall · Livestreamed worldwide"

    stats: list[Stat] = [
        {"value": "100%", "label": "Proceeds donated"},
        {"value": "24", "label": "New performers"},
        {"value": "3", "label": "Aid partners"},
        {"value": "$48k", "label": "Raised since FF1"},
    ]

    collaborators: list[Partner] = [
        {
            "name": "Project Hope",
            "image": "/project_hope.svg",
        },
        {
            "name": "Randomizer Brasil",
            "image": "/RBR.png",
        },
        {
            "name": "KHDE",
            "image": "/KHDE.png",
        },
        {
            "name": "Speedrun Kingdom Hearts Francophone",
            "image": "/SKHF.gif",
        },
        {
            "name": "SpeedrunsEspanol",
            "image": "/SRE.png",
        },
    ]

    # Ready for the homepage banner; the section is commented out until we have real sponsors.
    sponsors: list[Partner] = [
        {
            "name": "Square Enix",
            "image": "/square_enix.png",
        },
        {
            "name": "Floating Grip",
            "image": "/floating_grip.webp",
        },
    ]
