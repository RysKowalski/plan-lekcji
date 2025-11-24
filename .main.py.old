import yaml
from colorama import Fore, Style
from datetime import datetime, time
from typing import Literal
# example lesson: [{"czas":"08:00-08:45", "lekcja":"polski"}]

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


DAYS: list[tuple[WeekDays, str]] = [
    ("po", "====== PONIEDZIAŁEK ======"),
    ("wt", "========= WTOREK ========="),
    ("sr", "========= ŚRODA =========="),
    ("cz", "======== CZWARTEK ========"),
    ("pi", "========= PIĄTEK ========="),
]

ALL_DAYS: list[WeekDays] = ["po", "wt", "sr", "cz", "pi", "so", "ni"]


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


def load_data() -> dict[str, list[dict[str, str]]]:
    with open("lessons.yaml", "r") as file:
        data: dict[str, list[dict]] = yaml.safe_load(file)

    for key in data.keys():
        data[key] = [
            {
                "lekcja": elem["lekcja"],
                "sala": elem["sala"],
            }
            for elem in data[key]
        ]
    return data


def wizualizuj_lekcje(plan: list[dict[str, str]], highlight: bool = False) -> None:
    """Wizualizuje listę lekcji w formacie tabeli w terminalu."""
    if not plan:
        print("Brak lekcji do wyświetlenia.")
        return

    szer_czas = 11
    szer_lekcja = max(min(len(elem["lekcja"]), 20) for elem in plan)
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

    for i, elem in enumerate(plan):
        czas = LESSONS[i + 1].ljust(szer_czas)
        lekcja = elem["lekcja"][:20].ljust(szer_lekcja)
        sala = f" {elem['sala']}".ljust(4)
        numer = i + 1
        if highlight and get_current_lesson_index() == i + 1:
            print(
                f"{Fore.LIGHTRED_EX}| {Fore.BLUE}{numer}{Fore.LIGHTRED_EX} | {Fore.GREEN}{czas}{Fore.LIGHTRED_EX} | {Fore.BLUE}{lekcja}{Fore.LIGHTRED_EX} | {Fore.GREEN}{sala}{Fore.LIGHTRED_EX} |{Fore.LIGHTCYAN_EX}"
            )
        else:
            print(f"| {numer} | {czas} | {lekcja} | {sala} |")
    print(separator)


def main():
    plan = load_data()
    current_day: WeekDays = get_current_weekday()

    for day in DAYS:
        highlight: bool = day[0] == current_day
        if highlight:
            print(Fore.LIGHTCYAN_EX, end="")
        print(day[1])
        wizualizuj_lekcje(plan[day[0]], highlight)
        print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
