import json
import os
from datetime import datetime, time
from typing import Literal, cast

from colorama import Back, Fore

from data_things import updateData
from jsontype import Colors, Lessons, SortedProcessedLessons
from run_periodic import run_once_per_week

WeekDays = Literal["po", "wt", "sr", "cz", "pi", "so", "ni"]

LESSONS: dict[int, str] = {
    1: "08:00-08:45",
    2: "08:55-09:40",
    3: "09:55-10:35",
    4: "10:50-11:35",
    5: "11:45-12:30",
    6: "12:40-13:25",
    7: "13:40-14:25",
    8: "14:35-15:20",
    9: "15:30-16:15",
}

VISIBLE_DAYS: list[Literal["po", "wt", "sr", "cz", "pi"]] = [
    "po",
    "wt",
    "sr",
    "cz",
    "pi",
]

DAYS: dict[WeekDays, str] = {
    "po": f"{'=' * 17} PONIEDZIAŁEK {'=' * 18}",
    "wt": f"{'=' * 21} WTOREK {'=' * 20}",
    "sr": f"{'=' * 21} ŚRODA {'=' * 21}",
    "cz": f"{'=' * 20} CZWARTEK {'=' * 19}",
    "pi": f"{'=' * 21} PIĄTEK {'=' * 20}",
    "so": "",
    "ni": "",
}


def rgb(
    mode: Literal["fg", "bg", "both"],
    fg: tuple[int, int, int] = (0, 0, 0),
    bg: tuple[int, int, int] = (0, 0, 0),
) -> str:
    fr, fg_, fb = fg
    br, bg_, bb = bg
    if mode == "both":
        return f"\033[38;2;{fr};{fg_};{fb}m\033[48;2;{br};{bg_};{bb}m"
    elif mode == "fg":
        return f"\033[38;2;{fr};{fg_};{fb}m"
    elif mode == "bg":
        return f"\033[48;2;{br};{bg_};{bb}m"


END_MODIFIER: str = "\033[0m"

BASE_COLORS: Colors = {
    "base": Fore.WHITE,
    "lesson": Fore.WHITE,
    "naglowek": Fore.YELLOW,
    "number": Fore.WHITE,
    "room": Fore.WHITE,
    "time": Fore.WHITE,
}

HIGHTLIGHT_DAY: Colors = {
    "base": Fore.LIGHTCYAN_EX,
    "lesson": Fore.BLUE,
    "naglowek": Fore.LIGHTYELLOW_EX,
    "number": Fore.CYAN,
    "room": Fore.LIGHTGREEN_EX,
    "time": Fore.GREEN,
}

_HIGHTLIGHT_COLORS: str = rgb("both", (0, 255, 255), (0, 99, 0))
HIGHTLIGHT_COLORS: Colors = {
    "base": _HIGHTLIGHT_COLORS,
    "lesson": _HIGHTLIGHT_COLORS,
    "naglowek": _HIGHTLIGHT_COLORS,
    "number": _HIGHTLIGHT_COLORS,
    "room": _HIGHTLIGHT_COLORS,
    "time": _HIGHTLIGHT_COLORS,
}

DELETE_MODYFIER: Colors = {
    "base": f"{Back.RED}",
    "lesson": rgb("both", (61, 255, 233), (204, 4, 3)),
    "naglowek": f"{Back.RED}",
    "number": f"{Back.RED}",
    "room": f"{Back.RED}",
    "time": f"{Back.RED}",
}

_CHANGED_MODYFIER: str = rgb("bg", bg=(4, 81, 105))
CHANGED_MODYFIER: Colors = {
    "base": _CHANGED_MODYFIER,
    "lesson": rgb("fg", fg=(0, 255, 37)) + _CHANGED_MODYFIER,
    "naglowek": _CHANGED_MODYFIER,
    "number": _CHANGED_MODYFIER,
    "room": _CHANGED_MODYFIER,
    "time": _CHANGED_MODYFIER,
}


def get_current_lesson_index() -> int:
    """Return the index of the current lesson based on current system time.
    If no lesson is ongoing, return the next upcoming lesson index.
    Return -1 if all lessons for the day have ended.
    """
    now: time = datetime.now().time()
    lessons_sorted = sorted(
        LESSONS.items(), key=lambda x: time.fromisoformat(x[1].split("-")[0])
    )

    for index, period in lessons_sorted:
        start_str, end_str = period.split("-")
        start = time.fromisoformat(start_str)
        end = time.fromisoformat(end_str)

        if start <= now <= end:
            return index
        if now < start:
            return index

    return -1


def get_current_weekday() -> WeekDays:
    day = datetime.today().weekday()
    return list(DAYS.keys())[day]


def load_data() -> SortedProcessedLessons:
    with open("lessons.json", "r") as file:
        data: Lessons = json.load(file)
    return data["days"]


def get_terminal_width() -> int:
    return os.get_terminal_size().columns


def merge_colors(colors1: Colors, colors2: Colors):
    new_colors: Colors = colors1.copy()
    for color in new_colors.keys():
        new_colors[color] += colors2[color]
    return new_colors


def visualize(
    plan: SortedProcessedLessons,
    base_colors: Colors = BASE_COLORS,
    highlight_colors: Colors = HIGHTLIGHT_COLORS,
    deleted_colors: Colors = DELETE_MODYFIER,
    moved_colors: Colors = CHANGED_MODYFIER,
    hightlight_day: Colors = HIGHTLIGHT_DAY,
):
    current_day: WeekDays = get_current_weekday()

    szer_czas = 11
    szer_lekcja = 20
    szer_sala = 4
    szer_numer = 1

    naglowek_czas = "CZAS".ljust(szer_czas)
    naglowek_lekcja = "LEKCJA".ljust(szer_lekcja)
    naglowek_sala = "SALA"
    naglowek_numer = "N"
    separator = f"+{'-' * (szer_numer + 2)}+{'-' * (szer_czas + 2)}+{'-' * (szer_lekcja + 2)}+{'-' * (szer_sala + 2)}+"

    plan_width: int = len(separator)
    term_width: int = get_terminal_width()
    change_reason_width: int = term_width - plan_width - 1

    for day in VISIBLE_DAYS:
        highlight: bool = day == current_day
        if highlight:
            colors: Colors = hightlight_day
        else:
            colors: Colors = base_colors

        print(
            colors["naglowek"],
            DAYS[cast(WeekDays, day)],
            END_MODIFIER,
            sep="",
        )

        print(f"{colors['base']}{separator}{END_MODIFIER}")
        print(
            f"{colors['base']}| ",
            f"{colors['number']}{naglowek_numer}",
            f"{colors['base']} | ",
            f"{colors['time']}{naglowek_czas}",
            f"{colors['base']} | ",
            f"{colors['lesson']}{naglowek_lekcja}",
            f"{colors['base']} | ",
            f"{colors['room']}{naglowek_sala}",
            f"{colors['base']} |{END_MODIFIER}",
            sep="",
        )
        print(f"{colors['base']}{separator}{END_MODIFIER}")

        for lesson in sorted(plan[cast(WeekDays, day)], key=lambda x: x["number"]):
            if highlight and get_current_lesson_index() == lesson["number"]:
                lesson_colors: Colors = highlight_colors
            else:
                lesson_colors: Colors = colors
            if lesson["change"] == 1:
                lesson_colors = merge_colors(lesson_colors, deleted_colors)
            elif lesson["change"] == 2 or lesson["change"] == 3:
                lesson_colors = merge_colors(lesson_colors, moved_colors)

            print(
                f"{lesson_colors['base']}| ",
                f"{lesson_colors['number']}{lesson['number']}",
                f"{lesson_colors['base']} | ",
                f"{lesson_colors['time']}{lesson['display_time']}",
                f"{lesson_colors['base']} | ",
                f"{lesson_colors['lesson']}{lesson['lesson'][:20].ljust(20)}",
                f"{lesson_colors['base']} | ",
                f"{lesson_colors['room']} {lesson['room']} ",
                f"{lesson_colors['base']} |{END_MODIFIER}",
                f" {lesson['change_reason'][:change_reason_width]}",
                sep="",
            )

        print(f"{colors['base']}{separator}{END_MODIFIER}")
        print()


def main():
    lessons = load_data()
    visualize(lessons)


if __name__ == "__main__":
    run_once_per_week(updateData)
    os.system("clear")
    main()
