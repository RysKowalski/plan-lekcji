import json
from datetime import datetime
import os
from jsontype import (
    RawData,
    SingleLesson,
    ProcessedLessons,
    SingleProcessedLesson,
    SortedProcessedLessons,
)
from typing import Literal


def load_data() -> RawData:
    with open("raw.json", "r") as file:
        data: RawData = json.load(file)
    return data


def get_weekday(date: str) -> Literal["po", "wt", "sr", "cz", "pi"]:
    names: list = ["po", "wt", "sr", "cz", "pi", "pi", "pi"]
    return names[datetime.strptime(date, "%Y-%m-%d").weekday()]


def process_lesson(raw_lesson: SingleLesson) -> SingleProcessedLesson:
    change: int = 0
    if raw_lesson["Change"] is not None:
        change = 1

    number = 0
    lesson: str = "None"
    start_time: str = "01:01"
    end_time: str = "01:02"
    display_time: str = "01:01-01:02"
    room: str = "00"
    date: str = "2025-01-01"

    if change == 0:
        lesson = raw_lesson["Subject"]["Name"]
        start_time = raw_lesson["TimeSlot"]["Start"]
        end_time = raw_lesson["TimeSlot"]["End"]
        display_time = raw_lesson["TimeSlot"]["Display"]
        date = raw_lesson["DateAt"]
        number = raw_lesson["TimeSlot"]["Position"]
        if raw_lesson["Room"] is not None:
            room = raw_lesson["Room"]["Code"]

    return {
        "lesson": lesson,
        "number": number,
        "start_time": start_time,
        "end_time": end_time,
        "display_time": display_time,
        "room": room,
        "change": change,
        "date": date,
    }


def process_data(raw_data: RawData) -> ProcessedLessons:
    processed_lessons: ProcessedLessons = []
    for raw_lesson in raw_data:
        processed_lessons.append(process_lesson(raw_lesson))
    return processed_lessons


def sort_lessons(unsorted_lessons: ProcessedLessons) -> SortedProcessedLessons:
    sorted_lessons: SortedProcessedLessons = {
        "po": [],
        "wt": [],
        "sr": [],
        "cz": [],
        "pi": [],
        "last_update": str(datetime.now()),
    }

    for lesson in unsorted_lessons:
        sorted_lessons[get_weekday(lesson["date"])].append(lesson)

    return sorted_lessons


def save_lessons(lessons: SortedProcessedLessons):
    with open("lessons.json", "w") as file:
        json.dump(lessons, file, indent="  ")


def main():
    os.system("cd js_stuff && node main.js")
    save_lessons(sort_lessons(process_data(load_data())))


if __name__ == "__main__":
    main()
