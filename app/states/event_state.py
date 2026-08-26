from typing import TypedDict

import reflex as rx


class Partner(TypedDict):
    name: str
    role: str
    note: str
    icon: str
    image: str


class Stat(TypedDict):
    value: str
    label: str


class EventState(rx.State):
    event_name: str = "Fresh Faces 4"
    logo_image: str = ""
    logo_icon: str = "heart"
    tagline: str = "A Charity Showcase for Ukraine"
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
            "name": "Keyblade Collective",
            "role": "Creative direction",
            "note": "Stained-glass stage art and the luminous heart centerpiece.",
            "icon": "palette",
            "image": "",
        },
        {
            "name": "Sunflower Sound Lab",
            "role": "Live audio",
            "note": "Full mix, monitors and broadcast audio, donated in full.",
            "icon": "audio-lines",
            "image": "",
        },
        {
            "name": "Nova Youth Choir",
            "role": "Opening set",
            "note": "Forty voices opening the night with Ukrainian folk arrangements.",
            "icon": "mic-vocal",
            "image": "",
        },
        {
            "name": "Ribbon & Arc Studio",
            "role": "Stage design",
            "note": "Blue-and-yellow ribbon arcs sweeping across the proscenium.",
            "icon": "brush",
            "image": "",
        },
        {
            "name": "Second Star Media",
            "role": "Film & livestream",
            "note": "Six-camera capture so friends abroad can watch live.",
            "icon": "video",
            "image": "",
        },
        {
            "name": "Volunteers of Ward 7",
            "role": "Hosts & logistics",
            "note": "Doors, seating, merch table and a very warm welcome.",
            "icon": "hand-heart",
            "image": "",
        },
    ]

    endorsers: list[Partner] = [
        {
            "name": "Maryna Kovalenko",
            "role": "Kyiv relief coordinator",
            "note": "\u201cEvery seat filled here becomes a warm winter for a family back home.\u201d",
            "icon": "quote",
            "image": "",
        },
        {
            "name": "Hearts Forward Alliance",
            "role": "Humanitarian partner",
            "note": "\u201cFresh Faces proves new artists can move real resources, fast.\u201d",
            "icon": "shield-check",
            "image": "",
        },
        {
            "name": "Council for the Arts",
            "role": "Community endorsement",
            "note": "\u201cA model for youth-led fundraising with genuine artistic ambition.\u201d",
            "icon": "award",
            "image": "",
        },
    ]

    sponsors: list[Partner] = [
        {
            "name": "Lumina Instruments",
            "role": "Radiant tier",
            "note": "Backline, strings and a matching gift up to $10,000.",
            "icon": "crown",
            "image": "",
        },
        {
            "name": "Northlight Coffee",
            "role": "Starlight tier",
            "note": "Green room hospitality for every performer and volunteer.",
            "icon": "coffee",
            "image": "",
        },
        {
            "name": "Arcline Print Co.",
            "role": "Starlight tier",
            "note": "Posters, programmes and the ribbon banner wall.",
            "icon": "printer",
            "image": "",
        },
        {
            "name": "Harbor Community Bank",
            "role": "Keystone tier",
            "note": "Covering venue costs so donations pass through untouched.",
            "icon": "landmark",
            "image": "",
        },
    ]
