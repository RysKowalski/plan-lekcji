import yaml
# example lesson: [{"czas":"08:00-08:45", "lekcja":"polski"}]

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

DAYS: list[tuple[str, str]] = [
    ("po", "=== PONIEDZIAŁEK ==="),
    ("wt", "====== WTOREK ======"),
    ("sr", "====== ŚRODA ======="),
    ("cz", "===== CZWARTEK ====="),
    ("pi", "====== PIĄTEK ======"),
]


def load_data() -> dict[str, list[dict[str, str]]]:
    with open("lessons.yaml", "r") as file:
        data: dict[str, list[dict]] = yaml.safe_load(file)

    for key in data.keys():
        data[key] = [
            {
                "lekcja": elem["lekcja"],
                "czas": LESSONS[elem["czas"]],
                "sala": elem["sala"],
            }
            for elem in data[key]
        ]
    return data


def wizualizuj_lekcje(plan: list[dict[str, str]]) -> None:
    """Wizualizuje listę lekcji w formacie tabeli w terminalu."""
    if not plan:
        print("Brak lekcji do wyświetlenia.")
        return

    szer_czas = max(len(elem["czas"]) for elem in plan)
    szer_lekcja = max(min(len(elem["lekcja"]), 20) for elem in plan)
    szer_sala = 4
    szer_numer = 2

    naglowek_czas = "CZAS".ljust(szer_czas)
    naglowek_lekcja = "LEKCJA".ljust(szer_lekcja)
    naglowek_sala = "SALA"
    naglowek_numer = "NR"
    separator = f"+{'-' * (szer_numer + 2)}+{'-' * (szer_czas + 2)}+{'-' * (szer_lekcja + 2)}+{'-' * (szer_sala + 2)}+"

    print(separator)
    print(
        f"| {naglowek_numer} | {naglowek_czas} | {naglowek_lekcja} | {naglowek_sala} |"
    )
    print(separator)

    for i, elem in enumerate(plan):
        czas = elem["czas"].ljust(szer_czas)
        lekcja = elem["lekcja"][:20].ljust(szer_lekcja)
        sala = elem["sala"].ljust(4)
        numer = i
        print(f"| {numer + 1} | {czas} | {lekcja} | {sala} |")

    print(separator)


if __name__ == "__main__":
    plan = load_data()

    for day in DAYS:
        print(day[1])
        wizualizuj_lekcje(plan[day[0]])
        print()
