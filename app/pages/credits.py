import os

from typing import TypedDict

import reflex as rx

from app.components.page_shell import page_heading, page_shell
from app.components.brand_glyphs import twitch_glyph

class Credit(TypedDict):
    name: str
    twitch_name: str
    role: str
    role_class: str
    twitch_channel: str
    icon: str


# Use the latest, full raw_credits_list and add BOTH name and twitch_name to each credit entry.
RAW_CREDITS_LIST: list[dict] = [
    {"name": "roromaniac", "twitch_name": "roromaniac8", "role": "Director", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "LittleHerdez", "twitch_name": "littleherdez", "role": "International Coordinator", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "WallpeSH", "twitch_name": "wallpesh", "role": "Community Outreach", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "Kaeldiar", "twitch_name": "kaeldiar", "role": "Bookkeeper", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "IgnitedTNT", "twitch_name": "ignitedtnt", "role": "Bookkeeper", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "Darknesm1st", "twitch_name": "darknesm1st", "role": "Tutorial Maker", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "Kallat", "twitch_name": "kallat11", "role": "Async Manager", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "IBA_ALLDAY", "twitch_name": "ibaallday", "role": "Community Outreach", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "WarehouseJesus", "twitch_name": "warehousejesus", "role": "Production Lead", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "bahb", "twitch_name": "bahb", "role": "Tournament Organizer", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "Uki", "twitch_name": "UkiMiyoshi", "role": "Tournament Organizer", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "moko", "twitch_name": "mokonasakaidono", "role": "Tournament Organizer", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "tippyturner", "twitch_name": "tippyturner", "role": "Tournament Organizer", "role_class": "Tournament Organizer", "image": "/ukraine_heart.webp"},
    {"name": "Codename_Geek", "twitch_name": "codename_geek", "role": "Layout Designer and Tournament Designer", "role_class": "Production", "image": "/ukraine_heart.webp"},
    # {"name": "CoreySG9", "twitch_name": "coreysg9", "role": "Video Editor", "role_class": "Production", "image": "/ukraine_heart.webp"},
    # {"name": "DoubleADewi", "twitch_name": "doubleadewi", "role": "Video Editor", "role_class": "Production", "image": "/ukraine_heart.webp"},
    # {"name": "RyuuRush", "twitch_name": "ryuurush", "role": "Video Editor", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "dallin", "twitch_name": "dallin1016", "role": "Graphic Designer", "role_class": "Production", "image": "/ukraine_heart.webp"},
    # {"name": "Chemigoku", "twitch_name": "chemigoku", "role": "Caster (ES)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    # {"name": "CapitanBublo", "twitch_name": "capitanbublo", "role": "Caster (ES)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "Tso15", "twitch_name": "tso15", "role": "Caster (PT)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "CesarMartins", "twitch_name": "cesarmartins12", "role": "Caster (PT)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "S0nzero", "twitch_name": "s0nzero", "role": "Caster (FR)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "c3pown", "twitch_name": "c3pown", "role": "Caster (DE)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "Flowleyd", "twitch_name": "flowleyd", "role": "Caster (DE)", "role_class": "Caster", "image": "/ukraine_heart.webp"},
    {"name": "NobodyDaxian", "twitch_name": "nobodydaxian", "role": "Event Endorser (code: 'dax')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "LanzTheMaster", "twitch_name": "lanzthemaster", "role": "Event Endorser (code: 'lanz')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "KeyOfTime15", "twitch_name": "keyoftime15", "role": "Event Endorser (code: 'key')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "BioRoxas", "twitch_name": "bioroxas", "role": "Event Endorser (code: 'bio')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "Skraxx", "twitch_name": "OG_Skraxx", "role": "Event Endorser (code: 'skraxx')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "KHGuides", "twitch_name": "KHGuides", "role": "Event Endorser (code: 'guides')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    # {"name": "RegularPat", "twitch_name": "regularpatyt", "role": "Event Endorser (code: 'regularpat')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "RadiantGardeners", "twitch_name": "radiantgardeners", "role": "Event Endorser (code: 'rg')", "role_class": "Production", "image": "/ukraine_heart.webp"},
    {"name": "Lindsey", "twitch_name": "projecthopeorg", "role": "Project Hope Fundraising Lead", "role_class": "Charity", "image": "/ukraine_heart.webp"},
]

# Convert to the Credit type and populate twitch_channel field.
CREDITS: list[Credit] = []

for entry in RAW_CREDITS_LIST:
    # If a custom asset exists for this person in "assets", use the real filename
    asset_files = os.listdir("assets")
    all_names_in_assets = [os.path.splitext(name)[0].lower() for name in asset_files]
    if entry["name"].lower() in all_names_in_assets:
        match_idx = all_names_in_assets.index(entry["name"].lower())
        asset_icon = f"/{asset_files[match_idx]}"
    elif entry["twitch_name"].lower() in all_names_in_assets:
        match_idx = all_names_in_assets.index(entry["twitch_name"].lower())
        asset_icon = f"/{asset_files[match_idx]}"
    else:
        asset_icon = entry.get("image", "/ukraine_heart.webp")

    CREDITS.append({
        "name": entry["name"],
        "twitch_name": entry["twitch_name"],
        "role": entry["role"],
        "role_class": entry["role_class"],
        "twitch_channel": f"https://www.twitch.tv/{entry['twitch_name']}",
        "icon": asset_icon,
    })


def _credit_card(credit: Credit) -> rx.Component:
    # All sections get fixed size constraints and alignment for even-ness.
    return rx.el.article(
        rx.el.div(
            rx.image(
                src=credit["icon"],
                alt="",
                class_name="w-full h-full object-cover rounded-full",
            ),
            # Fixed size, always perfect circle, consistent
            class_name="flex h-40 w-40 min-h-40 min-w-40 max-h-40 max-w-40 items-center justify-center rounded-full border border-amber-200/40 bg-amber-300/10 overflow-hidden mx-auto",
        ),
        rx.el.div(
            rx.el.div(
                credit["name"],
                class_name="block ff-menu-bold-font text-lg text-amber-100 text-center",
                style={"minHeight": "32px", "display": "flex", "alignItems": "center", "justifyContent": "center"},  # consistent min height for name
            ),
            rx.el.a(
                rx.el.span(
                    twitch_glyph(class_name="h-8 w-8 text-[#efe7ff] mr-1"),
                    rx.el.span(
                        credit["twitch_name"],
                        # Changed 'text-xs' (0.75rem) to 'text-base' (1rem, 2x) for larger text size
                        class_name="text-base text-purple-200/80 align-middle",
                        # If you want precise sizing, you could instead use style={"fontSize": "1.5rem"}
                    ),
                    class_name="inline-flex items-center justify-center",
                ),
                href=credit["twitch_channel"],
                target="_blank",
                class_name="block mt-1 mb-1 text-center transition-colors hover:text-amber-200",
                style={"minHeight": "36px", "display": "flex", "alignItems": "center", "justifyContent": "center"},  # twitch section consistent
            ),
            rx.el.div(
                credit["role"],
                class_name="ff-menu-font text-center text-sky-100/80 mt-2",
                style={"minHeight": "28px", "display": "flex", "alignItems": "center", "justifyContent": "center"},  # consistent min height for role
            ),
            rx.el.div(
                credit["role_class"],
                class_name="ff-data-font mt-3 rounded-full border border-amber-200/30 bg-amber-200/15 px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-amber-100 text-center",
                style={"minHeight": "30px", "display": "flex", "alignItems": "center", "justifyContent": "center"},  # force pill to be aligned
            ),
            class_name="flex flex-col items-center w-full px-0 gap-0",
            style={
                "width": "100%",
                "minHeight": "172px",  # 32 + 36 + 28 + 30 + spacing ≈ total
                "maxHeight": "172px",
                "justifyContent": "space-between",
            }
        ),
        class_name=(
            "flex flex-col items-center justify-between rounded-2xl border border-white/10 bg-white/[0.04] p-6 "
            "backdrop-blur-md transition-transform duration-300 hover:-translate-y-1 "
            "hover:border-sky-300/40 w-full h-full"
        ),
        style={
            "minWidth": "275px",    # Ensures every card has the same width and height in the grid!
            "maxWidth": "275px",
            "minHeight": "370px",
            "maxHeight": "370px",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "space-between",
        }
    )


def credits() -> rx.Component:
    return page_shell(
        page_heading(
            "The Friends that Power Fresh Faces 4",
            "Go drop a follow for the lovely people who make this event possible!",
        ),
        rx.el.div(
            rx.foreach(CREDITS, _credit_card),
            # Large screens: 6 columns. Progressively break down at lower breakpoints.
            class_name=(
                "grid grid-cols-1 gap-6 "
                "sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 "
                "items-stretch justify-center"
            ),
            style={
                "alignItems": "center",
                "justifyItems": "center",
                "width": "100vw",   # Take up as much horizontal space as possible
                "maxWidth": "100vw",
                "marginLeft": "calc(-50vw + 50%)",  # Center the full-width grid within a fixed-width parent
                "paddingLeft": "2vw",
                "paddingRight": "2vw",
                "boxSizing": "border-box",
            }
        ),
    )
