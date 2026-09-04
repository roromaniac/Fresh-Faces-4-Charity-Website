import reflex as rx

from app.states.window_state import LEFT_ITEMS, RIGHT_ITEMS, WindowItem, WindowState

# Shrink each pane title until the whole line fits inside the square.
_FIT_PANE_LABEL_JS = """
(() => {
  if (window.__ffPaneFit) return;
  window.__ffPaneFit = true;

  const MIN_PX = 7;
  let timer = 0;

  function fitOne(label) {
    const avail = label.clientWidth;
    const key = (label.textContent || "") + "@" + avail;
    if (label.dataset.ffFit === key) return;
    label.style.fontSize = "";
    const need = label.scrollWidth;
    if (avail && need > avail + 1) {
      const current = parseFloat(getComputedStyle(label).fontSize);
      label.style.fontSize = Math.max(MIN_PX, current * (avail / need) * 0.97) + "px";
    }
    label.dataset.ffFit = key;
  }

  function watchSlots() {
    document.querySelectorAll(".ff-pane-fit-slot").forEach((slot) => {
      const label = slot.querySelector(".ff-pane-fit-label");
      if (label) fitOne(label);
      if (!slot.__ffFitObs) {
        slot.__ffFitObs = true;
        ro.observe(slot);
      }
    });
  }

  function requestFit() {
    if (timer) return;
    timer = window.setTimeout(() => {
      timer = 0;
      watchSlots();
    }, 16);
  }

  const lastWidth = new WeakMap();
  const ro = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const width = entry.contentRect.width;
      if (lastWidth.get(entry.target) === width) continue;
      lastWidth.set(entry.target, width);
      const label = entry.target.querySelector(".ff-pane-fit-label");
      if (label) fitOne(label);
    }
  });

  const start = () => {
    watchSlots();
    new MutationObserver(requestFit).observe(document.body, {
      childList: true,
      subtree: true,
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(watchSlots);
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
"""


def _dots(count: int, active: int) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(count),
            lambda i: rx.el.span(
                class_name=rx.cond(
                    i == active,
                    "h-1.5 w-4 rounded-full bg-amber-200/90 transition-all duration-500",
                    "h-1.5 w-1.5 rounded-full bg-white/25 transition-all duration-500",
                )
            ),
        ),
        class_name="flex items-center justify-center gap-1",
    )


def _pane(item: WindowItem, index: int) -> rx.Component:
    # Title stays on one line; CSS/JS shrink the font so it never clips.
    # To make the image 30% bigger: 151px * 1.3 = 196.3px
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                rx.el.span(item["label"] + ": "),
                rx.el.span(
                    item["highlight"],
                    class_name="italic underline text-orange-500",
                ),
                class_name="ff-pane-fit-label ff-menu-font uppercase text-amber-200/90",
            ),
            class_name="ff-pane-fit-slot",
        ),
        rx.el.div(
            rx.image(
                src=item["image"],
                alt=item["label"],
                class_name=(
                    "h-[196.3px] w-[196.3px] object-cover rounded-xl "
                    "border border-amber-200/40 bg-amber-300/20 "
                    "drop-shadow-[0_0_33.6px_rgba(250,204,21,0.45)]"
                ),
            ),
            class_name=(
                "flex h-[196.3px] w-[196.3px] items-center justify-center "
                "rounded-xl border border-amber-200/30 bg-amber-300/10"
            ),
        ),
        rx.el.span(
            item["bottom_text"],
            class_name="ff-menu-font text-[13.65px] uppercase tracking-[0.231em] text-amber-200/70 w-full text-center",
        ),
        key=index,
        class_name=(
            "ff-pane-in flex h-full w-full min-w-0 flex-col items-center "
            "justify-center gap-3 px-3 pb-8 pt-3"
        ),
    )


def stained_window(
    item: WindowItem,
    index: int,
    count: int,
    on_click: rx.event.EventType,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="pointer-events-none absolute -inset-[3.15px] rounded-3xl bg-[conic-gradient(from_0deg,rgba(56,189,248,0.30),rgba(250,204,21,0.30),rgba(99,102,241,0.30),rgba(56,189,248,0.30))] blur-[13.65px] opacity-60 transition-opacity duration-500 group-hover:opacity-95"
        ),
        rx.el.div(
            rx.el.div(
                class_name="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1.365px,transparent_1.365px),linear-gradient(90deg,rgba(255,255,255,0.05)_1.365px,transparent_1.365px)] bg-[size:29.4px_29.4px] opacity-50"
            ),
            rx.el.div(
                class_name="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.14),transparent_60%)]"
            ),
            rx.el.div(
                _pane(item, index),
                rx.el.div(
                    _dots(count, index),
                    class_name="absolute inset-x-0 bottom-2 flex justify-center",
                ),
                class_name="relative h-full w-full",
            ),
            class_name="ff-glass-window relative h-full w-full overflow-hidden rounded-2xl border border-white/15 bg-slate-900/60 backdrop-blur-md",
        ),
        on_click=on_click,
        # 35% bigger: w-52 * 1.05 ≈ w-54.5, sm:w-58 * 1.05 ≈ sm:w-60.9, etc.
        class_name=(
            "group relative aspect-square w-[13.625rem] shrink-0 cursor-pointer p-[0.079rem] "  # w-52*1.05=54.6rem/4=13.65rem, but tailwind non std, so w-[13.625rem]
            "transition-transform duration-500 hover:scale-[1.04] "
            "sm:w-[15.225rem] md:w-[16.275rem] lg:w-[20.475rem] xl:w-[23.205rem]"
        ),
        style={"max_width": "100%"},
    )


def left_window() -> rx.Component:
    return stained_window(
        WindowState.left_item,
        WindowState.left_index,
        len(LEFT_ITEMS),
        WindowState.next_left,
    )


def right_window() -> rx.Component:
    return stained_window(
        WindowState.right_item,
        WindowState.right_index,
        len(RIGHT_ITEMS),
        WindowState.next_right,
    )


def window_rotation_timer() -> rx.Component:
    return rx.fragment(
        rx.script(_FIT_PANE_LABEL_JS),
        rx.moment(
            interval=WindowState.rotate_ms,
            on_change=WindowState.rotate_windows,
            class_name="hidden",
        ),
    )
