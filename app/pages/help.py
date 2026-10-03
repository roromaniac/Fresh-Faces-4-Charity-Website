import reflex as rx

from app.components.page_shell import page_heading, page_shell


def _faq_item(question: str, answer: rx.Component) -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            rx.el.span(
                [
                    rx.el.span(
                        question,
                        class_name="",
                    ),
                    rx.el.span(
                        "▼",
                        class_name="ml-3 inline-block text-base text-white/70 align-middle",
                        aria_hidden="true",
                    ),
                ],
                class_name="flex items-center justify-between w-full"
            ),
            class_name="ff-menu-bold-font cursor-pointer list-none py-3 text-lg text-white marker:content-none",
        ),
        rx.el.div(answer, class_name="pb-4"),
        class_name="rounded-xl border border-white/10 bg-white/[0.04] px-4",
    )


def help_page() -> rx.Component:
    return page_shell(
        page_heading(
            "FAQ",
            rx.el.span(
                [
                    "Setup, Eligibility, and Logistic Questions for Fresh Faces 4",
                    rx.el.br(),
                    "Don't see your question here? Ask us in ",
                    rx.el.a(
                        "#tourney-discussions",
                        href="https://discord.com/channels/712837252279173150/849862221777076224",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                        target="_blank",
                    ),
                    ".",
                ]
            ),
        ),
   
        rx.el.div(
            _faq_item(
                "What is Fresh Faces 4?",
                rx.el.p(
                    "Fresh Faces is a Kingdom Hearts 2 Randomizer tournament series aimed at celebrating the newcomers into our community. Fresh Faces 4 is casual, low-stakes KH2 rando racing against other new, casual rando enjoyers while raising money to help Ukrainian civilians afflicted by the Russo-Ukrainian war. Every participant that joins enforces the host to donate $5 to ",
                    rx.el.a(
                        "Project Hope's Ukraine Fund",
                        href="https://www.projecthope.org/emergency-response/ukraine/",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                    ),
                    " for every entrant up to 200 entrants ($1000), so please consider joining our celebration of the newest KH2 rando enjoyers for a great cause!",
                    class_name="ff-menu-font text-sky-50/90",
                ),
            ),
            _faq_item(
                "How do I get set up with the KH2 Randomizer?",
                rx.el.p(
                    "Please visit the ",
                    rx.el.a(
                        "KH2 Randomizer website",
                        href="https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                    ),
                    " for installation instructions for both Steam and Epic Games setup.",
                    class_name="ff-menu-font text-sky-50/90",
                ),
            ),
            _faq_item(
                "I'm just lost and I need help. What can I do?",
                rx.el.p(
                    rx.fragment(
                        "Your best bet to receive personalized help is by contacting me (",
                        rx.el.span("roromaniac", class_name="font-bold italic text-amber-200"),
                        ") directly on Discord! If for some reason I don't get back to you quickly, feel free to contact any other tournament organizer or reach out to #help or #tourney-discussions in the Kingdom Hearts II Randomizer Discord server!",
                    ),
                    class_name="ff-menu-font text-sky-50/90",
                ),
           
            ),
            _faq_item(
                "I have played in Fresh Faces before. Can I play again?",
                rx.el.p(
                    "Of course! However, the division you play independs on how well you did. To keep the Fresh Faces division populated by newcomers and more casual rando players, we have a ",
                    rx.el.a(
                        "lookup tool",
                        href="/tools#ff4-eligibility-lookup",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                    ),
                    " that lets you search which division you should play in for Fresh Faces 4. If you believe there has been a mistake, please contact roromaniac or another TO directly on Discord.",
                    class_name="ff-menu-font text-sky-50/90",
                ),
            ),
            _faq_item(
                "What are the Graduated Faces and Veteran divisions?",
                rx.el.p(
                    rx.fragment(
                        "The Veteran division is meant for players who like to play on critical difficulty and are ",
                        rx.el.span(
                            "VERY",
                            class_name="font-extrabold text-yellow-300",
                        ),
                        " familiar with competitive KH2 rando.",
                        rx.el.br(),
                        rx.el.br(),
                        "The Graduated Faces division is meant for players who have played in Fresh Faces before (or other beginner tournies like Beginner Bootcamp), that are now ineligible to join the Fresh Faces division, but still want to get involved in playing KH2 rando. Graduated Faces will have the same settings as the Fresh Faces, but will only include people who are ineligibile for Fresh Faces that also aren't experienced enough for the Veteran division.",
                    ),
                    class_name="ff-menu-font text-sky-50/90",
                ),
           
            ),
            _faq_item(
                "How do I sign up for Fresh Faces 4?",
                rx.el.p(
                    "There is an ",
                    rx.el.a(
                        "RSVP link",
                        href="https://docs.google.com/forms/d/e/1FAIpQLSeajRfsMMfNPaQdOEPPm7LjlP6Unzic2ehwbokVVxvgho5Yig/viewform?usp=header",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                    ),
                    "! You can also click the button in the navbar. As long as qualifiers are still going on, it is not too late to sign up!",
                    class_name="ff-menu-font text-sky-50/90",
                ),
            ),
            _faq_item(
                "How do I know I have properly set up for Fresh Faces 4?",
                rx.el.p(
                    "There is ",
                    rx.el.a(
                        "an interactive checklist",
                        href="/tools#ff4-checklist",
                        class_name="text-amber-200 underline decoration-amber-200/40 hover:text-amber-100",
                    ),
                    " available for you to check if you're ready!",
                    class_name="ff-menu-font text-sky-50/90",
                ),
            ),
            _faq_item(
                "What events provide progression points?",
                rx.el.div(
                    rx.el.ul(
                        rx.el.li(
                            rx.el.span("Collect an Ansem Report:", class_name="font-bold text-amber-200"),
                            " 1",
                        ),
                        rx.el.li(
                            rx.el.span("Levels", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Level 10: 0"),
                                rx.el.li("Level 20: 0"),
                                rx.el.li("Level 30: 1"),
                                rx.el.li("Level 40: 0"),
                                rx.el.li("Level 50: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Drives", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Drive Level 2: 0"),
                                rx.el.li("Drive Level 3: 0"),
                                rx.el.li("Drive Level 4: 1"),
                                rx.el.li("Drive Level 5: 0"),
                                rx.el.li("Drive Level 6: 1"),
                                rx.el.li("Drive Level 7: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Simulated Twilight Town (STT)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("STT Enter: 0"),
                                rx.el.li("Olette Munny Pouch: 0"),
                                rx.el.li("Twilight Thorn: 1"),
                                rx.el.li("Axel 1: 0"),
                                rx.el.li("Setzer: 0"),
                                rx.el.li("Mansion Computer Room: 0"),
                                rx.el.li("Axel 2: 2"),
                                rx.el.li("Data Roxas: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Twilight Town (TT)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Twilight Town Enter: 0"),
                                rx.el.li("Station Dusk Fight: 0"),
                                rx.el.li("Mysterious Tower: 1"),
                                rx.el.li("Sandlot Fight: 0"),
                                rx.el.li("Mansion Fight: 0"),
                                rx.el.li("Betwixt and Between: 2"),
                                rx.el.li("Data Axel: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Hollow Bastion (HB)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Hollow Bastion Enter: 0"),
                                rx.el.li("Bailey Fight: 0"),
                                rx.el.li("Ansem's Study Computer: 0"),
                                rx.el.li("Corridors Fight: 1"),
                                rx.el.li("Dancers Fight: 0"),
                                rx.el.li("Demyx: 0"),
                                rx.el.li("Final Fantasy Fights: 0"),
                                rx.el.li("1000 Heartless: 2"),
                                rx.el.li("Sephiroth: 0"),
                                rx.el.li("Data Demyx: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Land of Dragons (LoD)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Land of Dragons Enter: 0"),
                                rx.el.li("Mission 3: 0"),
                                rx.el.li("Mountain Trail: 0"),
                                rx.el.li("Cave Fight: 0"),
                                rx.el.li("Summit Fight: 1"),
                                rx.el.li("Shan Yu: 1"),
                                rx.el.li("Antechamber Nobodies: 0"),
                                rx.el.li("Stormrider: 2"),
                                rx.el.li("Data Xigbar: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Beast's Castle (BC)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Beast's Castle Enter: 0"),
                                rx.el.li("Thresholder: 0"),
                                rx.el.li("Beast's Room: 0"),
                                rx.el.li("Dark Thorn: 1"),
                                rx.el.li("Ballroom Dragoons Fight: 0"),
                                rx.el.li("Xaldin: 2"),
                                rx.el.li("Data Xaldin: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Olympus Coliseum (OC)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Olympus Coliseum Enter: 0"),
                                rx.el.li("Cerberus: 0"),
                                rx.el.li("Phil's Urns: 0"),
                                rx.el.li("Demyx: 0"),
                                rx.el.li("Pete: 0"),
                                rx.el.li("Hydra: 1"),
                                rx.el.li("Auron Statue: 0"),
                                rx.el.li("Hades: 2"),
                                rx.el.li("AS Zexion: 0"),
                                rx.el.li("Data Zexion: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Disney Castle (DC)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Disney Castle Enter: 0"),
                                rx.el.li("Minnie Escort: 0"),
                                rx.el.li("Old Pete: 1"),
                                rx.el.li("Timeless River Windows: 0"),
                                rx.el.li("Boat Pete: 0"),
                                rx.el.li("Pete: 2"),
                                rx.el.li("AS Marluxia: 0"),
                                rx.el.li("Data Marluxia: 0"),
                                rx.el.li("Lingering Will: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Port Royal (PR)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Port Royal Enter: 0"),
                                rx.el.li("Town Fight: 0"),
                                rx.el.li("1 Minute Fight: 1"),
                                rx.el.li("Boat Medallion: 0"),
                                rx.el.li("Boat Barrels: 0"),
                                rx.el.li("Barbossa: 1"),
                                rx.el.li("Grim Reaper 1: 0"),
                                rx.el.li("First Medallion Gambler: 0"),
                                rx.el.li("Grim Reaper 2: 2"),
                                rx.el.li("Data Luxord: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Agrabah (AG)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Agrabah Enter: 0"),
                                rx.el.li("Abu Minigame: 0"),
                                rx.el.li("Chasm of Challenges: 0"),
                                rx.el.li("Treasure Room: 0"),
                                rx.el.li("Twin Lords: 1"),
                                rx.el.li("Carpet Magic: 0"),
                                rx.el.li("Genie Jafar: 2"),
                                rx.el.li("AS Lexaeus: 0"),
                                rx.el.li("Data Lexaeus: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Halloween Town (HT)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Halloween Town Enter: 0"),
                                rx.el.li("Candy Cane Lane Fight: 0"),
                                rx.el.li("Prison Keeper: 0"),
                                rx.el.li("Oogie Boogie: 1"),
                                rx.el.li("Lock, Shock, Barrel: 0"),
                                rx.el.li("Presents Minigame: 0"),
                                rx.el.li("Experiment: 2"),
                                rx.el.li("AS Vexen: 0"),
                                rx.el.li("Data Vexen: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Pride Lands (PL)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Pride Lands Enter: 0"),
                                rx.el.li("Talking to Simba: 0"),
                                rx.el.li("Hyenas 1: 0"),
                                rx.el.li("Scar: 1"),
                                rx.el.li("Hyenas 2: 0"),
                                rx.el.li("Groundshaker: 2"),
                                rx.el.li("Data Saix: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Space Paranoids (SP)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Space Paranoids Enter: 0"),
                                rx.el.li("Screens: 0"),
                                rx.el.li("Hostile Program: 1"),
                                rx.el.li("Solar Sailer Fight: 0"),
                                rx.el.li("MCP: 2"),
                                rx.el.li("AS Larxene: 0"),
                                rx.el.li("Data Larxene: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Hundred Acre Wood (HAW)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Pooh's Howse Enter: 0"),
                                rx.el.li("Piglet's Howse Complete: 0"),
                                rx.el.li("Rabbit's Howse Complete: 1"),
                                rx.el.li("Kanga's Howse Complete: 0"),
                                rx.el.li("Spooky Cave Complete: 1"),
                                rx.el.li("Starry Hill Complete: 1"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Atlantica", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("Atlantica Tutorial: 0"),
                                rx.el.li("Ursula's Revenge: 0"),
                                rx.el.li("A New Day is Dawning: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("The World That Never Was (TWTNW)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("TWTNW Enter: 0"),
                                rx.el.li("Roxas: 0"),
                                rx.el.li("Xigbar: 1 (Vets Only)"),
                                rx.el.li("Luxord: 0"),
                                rx.el.li("Saix: 0"),
                                rx.el.li("Xemnas 1: 2 (Vets Only)"),
                                rx.el.li("Data Xemnas: 0"),
                                class_name="ml-4"
                            )
                        ),
                        rx.el.li(
                            rx.el.span("Cavern of Remembrance (CoR)", class_name="font-bold text-amber-200"),
                            rx.el.ul(
                                rx.el.li("CoR Enter: 0"),
                                rx.el.li("First Fight: 0"),
                                rx.el.li("Steam Valves: 0"),
                                rx.el.li("Second Fight: 2 (Vets Only)"),
                                rx.el.li("Transport to Remembrance: 0"),
                                class_name="ml-4"
                            )
                        ),
                        class_name="list-disc pl-4 flex flex-col gap-1"
                    ),
                    class_name="text-sky-50/90 ff-menu-font text-sm sm:text-base"
                ),
            ),
            class_name="flex w-full flex-col gap-3",
        ),
    )
