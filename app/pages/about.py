import reflex as rx

from app.components.page_shell import page_heading, page_shell


def about() -> rx.Component:
    return page_shell(
        page_heading(
            "About Fresh Faces 4",
            "A Mission Statement from Roro(maniac)",
        ),
        rx.el.article(
            rx.el.p(
                "Hi there! I'm Roman, but I go by roro or roromaniac on socials. I'm the director of the team that's presenting Fresh Faces 4, the fourth installment of a charity Kingdom Hearts 2 randomizer tournament that uplifts and celebrates the newest entrants of the KH2 randomizer community.",
                class_name="ff-menu-font mb-6 text-lg leading-relaxed text-sky-50/90",
            ),
            rx.el.p(
                "On February 24, 2022, Russia launched an incredibly violent, full-scale invasion into Ukraine over disputes about NATO involvement in Ukraine and a more concerning belief that Ukraine is an artificial state with citizens that are one with Russia, as opposed to being part of a sovereign nation.",
                class_name="ff-menu-font mb-6 text-lg leading-relaxed text-sky-50/90",
            ),
            rx.el.p(
                "While the world discusses the big picture (e.g., military support, global politics, trade), many Ukrainian civilians have lost their lives. For many more still living, the quality of their lives has considerably worsened. For the Ukrainian civilians who have lost their families and homes, big picture discussions and weaponry assistance do not provide appropriate aid for the common person. The actions of entities like Project Hope that focus on ",
                rx.el.span("humanitarian", class_name="italic text-amber-200"),
                " aid are the actions that ",
                rx.el.span("actually", class_name="italic text-amber-200"),
                " help the people who need it most. The continuous involvement Project Hope has in Ukraine further motivates civilians who have been helped to turn around and help those around them, yielding a compounding helping process.",
                class_name="ff-menu-font mb-6 text-lg leading-relaxed text-sky-50/90",
            ),
            rx.el.p(
                "Even if we are fortunate enough to reach a peaceful, stable state in the future, there will be so much recovery and healing to do. This will become harder to accomplish as both the conflict and Ukraine exit mainstream media and people's attention will turn elsewhere.",
                class_name="ff-menu-font mb-6 text-lg leading-relaxed text-sky-50/90",
            ),
            rx.el.p(
                "Fresh Faces has been a series that has allowed me to plug into Project Hope's mission in Ukraine while staying involved and growing in the KH2 randomizer community. I am incredibly grateful for the continued support we have received, and we thank you all in advance for taking the time to read about our mission and continue the support through our fourth event. We continue to raise money ",
                rx.el.span("and", class_name="font-bold italic text-amber-200"),
                " welcome hundreds of new KH2 rando enthusiasts independent of politics and violence. So, on behalf of the entire Fresh Faces 4 team, we hope that you consider joining us as a racer, donor, viewer, incentive runner, supporter, or any combination thereof as we embark on the fourth iteration of Fresh Faces.",
                class_name="ff-menu-font mb-8 text-lg leading-relaxed text-sky-50/90",
            ),
            rx.el.div(
                rx.el.p(
                    "Slava Ukraini,", 
                    class_name="ff-gummi-font text-amber-200 text-2xl"
                ),
                rx.el.p(
                    "roro...",
                    class_name="ff-menu-bold-font mt-1 ff-title-gradient text-2xl",
                    style={"backgroundClip": "text", "WebkitTextFillColor": "transparent"},
                ),
                class_name="flex flex-col items-end",
            ),
       
            class_name="rounded-2xl border border-white/10 bg-white/[0.04] p-8 shadow-[0_0_40px_rgba(56,189,248,0.12)] backdrop-blur-md md:p-10",
        ),
    )
