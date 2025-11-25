import json
import os
from colorama import Fore, Style
from typing import Literal
from datetime import datetime, time
from jsontype import Lessons, ProcessedLessons, SortedProcessedLessons
from run_periodic import run_once_per_week
from data_things import main as update_data

WeekDays = Literal["po", "wt", "sr", "cz", "pi"]

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


DAYS: dict[WeekDays, str] = {
    "po": f"{'=' * 17} PONIEDZIAŁEK {'=' * 18}",
    "wt": f"{'=' * 21} WTOREK {'=' * 20}",
    "sr": f"{'=' * 21} ŚRODA {'=' * 21}",
    "cz": f"{'=' * 20} CZWARTEK {'=' * 19}",
    "pi": f"{'=' * 21} PIĄTEK {'=' * 20}",
}

ALL_DAYS: list[WeekDays] = ["po", "wt", "sr", "cz", "pi"]


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
    return ALL_DAYS[day]


def load_data() -> SortedProcessedLessons:
    with open("lessons.json", "r") as file:
        data: Lessons = json.load(file)
    return data["days"]


def wizualizuj_lekcje(plan: ProcessedLessons, highlight: bool = False) -> None:
    if not plan:
        print("Brak lekcji do wyświetlenia.")
        return

    szer_czas = 11
    szer_lekcja = 20
    szer_sala = 4
    szer_numer = 1

    naglowek_czas = "CZAS".ljust(szer_czas)
    naglowek_lekcja = "LEKCJA".ljust(szer_lekcja)
    naglowek_sala = "SALA"
    naglowek_numer = "N"
    separator = f"+{'-' * (szer_numer + 2)}+{'-' * (szer_czas + 2)}+{'-' * (szer_lekcja + 2)}+{'-' * (szer_sala + 2)}+"

    print(separator)
    print(
        f"| {naglowek_numer} | {naglowek_czas} | {naglowek_lekcja} | {naglowek_sala} |"
    )
    print(separator)

    sorted_plan: ProcessedLessons = sorted(plan, key=lambda x: x["number"])
    for elem in sorted_plan:
        czas = elem["display_time"]
        lekcja = elem["lesson"][:20].ljust(szer_lekcja)
        sala = f" {elem['room']}".ljust(4)
        numer = elem["number"]
        if elem["change"] == 1:
            print(Fore.RED, end="")
        if highlight and get_current_lesson_index() == elem["number"]:
            if elem["change"] == 1:
                print(
                    f"{Fore.RED}| {numer} | {Fore.GREEN}{czas}{Fore.RED} | {lekcja} | {sala} |{Fore.LIGHTCYAN_EX}"
                )
            else:
                print(
                    f"{Fore.LIGHTRED_EX}| {Fore.BLUE}{numer}{Fore.LIGHTRED_EX} | {Fore.GREEN}{czas}{Fore.LIGHTRED_EX} | {Fore.BLUE}{lekcja}{Fore.LIGHTRED_EX} | {Fore.GREEN}{sala}{Fore.LIGHTRED_EX} |{Fore.LIGHTCYAN_EX}"
                )
        else:
            print(f"| {numer} | {czas} | {lekcja} | {sala} |")
        if elem["change"] == 1:
            if highlight:
                print(Fore.LIGHTCYAN_EX, end="")
            else:
                print(Style.RESET_ALL, end="")
    print(separator)


def visualize(
    plan: SortedProcessedLessons,
    day_color: str = Fore.LIGHTYELLOW_EX,
    base_color: str = Fore.WHITE,
    highlight_current_day_base: str = Fore.LIGHTRED_EX,
    highlight_base_color: str = Fore.LIGHTCYAN_EX,
    hightlight_naglowek_color: str = Fore.WHITE,
    highlight_number_color: str = Fore.BLUE,
    highlight_time_color: str = Fore.GREEN,
    highlight_lesson_color: str = Fore.BLUE,
    highlight_room_color: str = Fore.GREEN,
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

    for day in plan.keys():
        print(separator)
        print(
            f"| {naglowek_numer} | {naglowek_czas} | {naglowek_lekcja} | {naglowek_sala} |"
        )
        print(separator)


def main():
    plan = load_data()
    current_day: WeekDays = get_current_weekday()

    for day in DAYS:
        highlight: bool = day[0] == current_day
        print(Fore.LIGHTYELLOW_EX, day[1], Style.RESET_ALL, sep="")
        if highlight:
            print(Fore.LIGHTCYAN_EX, end="")
        wizualizuj_lekcje(plan[day[0]], highlight)
        print(Style.RESET_ALL)


if __name__ == "__main__":
    # run_once_per_week(update_data)
    # os.system("clear")
    # main()
    lessons = load_data()
    visualize(lessons)
