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
            class_name="flex w-full flex-col gap-3",
        ),
    )
