from pathlib import Path
from datetime import date
from typing import Callable
import json

from jsontype import SortedProcessedLessons


def load_last_week() -> tuple[int, int] | None:
    with open("lessons.json", "r") as file:
        file_data: SortedProcessedLessons = json.load(file)
    data = file_data["last_update"].strip().split("-")
    if len(data) != 2:
        return None
    try:
        year = int(data[0])
        week = int(data[1])
        return year, week
    except ValueError:
        return None


def save_last_week(year: int, week: int) -> None:
    with open("lessons.json", "r") as file:
        data: SortedProcessedLessons = json.load(file)
    data["last_update"] = f"{year}-{week}"
    with open("lessons.json", "w") as file:
        json.dump(data, file)


def run_once_per_week(task: Callable[[], None]) -> None:
    current_date = date.today()
    current_year, current_week, _ = current_date.isocalendar()

    last = load_last_week()
    if last is None or last != (current_year, current_week):
        task()
        save_last_week(current_year, current_week)
