import json
import os
from datetime import datetime, time
from typing import Literal, cast


from data_things import updateData
from jsontype import Colors, Lessons, SortedProcessedLessons
from run_periodic import run_once_per_week
from colors import (
    END_MODIFIER,
    BASE_COLORS,
    HIGHTLIGHT_COLORS,
    DELETE_MODYFIER,
    CHANGED_MODYFIER,
    HIGHTLIGHT_DAY,
)

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


def main():
    updateAndClearScreen()
    lessons: SortedProcessedLessons = load_data()
    visualize(lessons)


def updateAndClearScreen():
    run_once_per_week(updateData)
    os.system("clear")


def load_data() -> SortedProcessedLessons:
    with open("lessons.json", "r") as file:
        data: Lessons = json.load(file)
    return data["days"]


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


def get_terminal_width() -> int:
    return os.get_terminal_size().columns


def merge_colors(colors1: Colors, colors2: Colors):
    new_colors: Colors = colors1.copy()
    for color in new_colors.keys():
        new_colors[color] += colors2[color]
    return new_colors


if __name__ == "__main__":
    main()
