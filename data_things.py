import json
from datetime import datetime, date
import os
import sys
from jsontype import (
    RawData,
    SingleLesson,
    ProcessedLessons,
    SingleProcessedLesson,
    Lessons,
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
        change = raw_lesson["Change"]["Type"]

    number = 0
    lesson: str = "None"
    start_time: str = "01:01"
    end_time: str = "01:02"
    room: str = "00"
    date: str = "2025-01-01"
    change_reason: str = ""

    if change == 0:
        lesson = raw_lesson["Subject"]["Name"]
        start_time = raw_lesson["TimeSlot"]["Start"]
        end_time = raw_lesson["TimeSlot"]["End"]
        number = raw_lesson["TimeSlot"]["Position"]
        date = raw_lesson["DateAt"]
        if raw_lesson["Room"] is not None:
            room = raw_lesson["Room"]["Code"]
    if change == 1:
        lesson = raw_lesson["Subject"]["Name"]
        start_time = raw_lesson["TimeSlot"]["Start"]
        end_time = raw_lesson["TimeSlot"]["End"]
        number = raw_lesson["TimeSlot"]["Position"]
        date = raw_lesson["DateAt"]
        if raw_lesson["Substitution"] is not None:
            change_reason = raw_lesson["Substitution"]["TeacherAbsenceEffectName"]
        if raw_lesson["Room"] is not None:
            room = raw_lesson["Room"]["Code"]
    if change == 2:
        lesson = raw_lesson["Subject"]["Name"]
        start_time = raw_lesson["TimeSlot"]["Start"]
        end_time = raw_lesson["TimeSlot"]["End"]
        number = raw_lesson["TimeSlot"]["Position"]
        date = raw_lesson["DateAt"]
        if raw_lesson["Substitution"] is not None:
            change_reason = raw_lesson["Substitution"]["TeacherAbsenceEffectName"]
        if raw_lesson["Room"] is not None:
            room = raw_lesson["Room"]["Code"]

    if change == 3:
        lesson = raw_lesson["Subject"]["Name"]
        if raw_lesson["Substitution"]["TimeSlot"] is not None:
            start_time = raw_lesson["Substitution"]["TimeSlot"]["Start"]
            end_time = raw_lesson["Substitution"]["TimeSlot"]["End"]
            number = raw_lesson["Substitution"]["TimeSlot"]["Position"]
        date = raw_lesson["Substitution"]["DateAt"]
        if raw_lesson["Substitution"] is not None:
            if raw_lesson["Substitution"]["TeacherAbsenceEffectName"] is not None:
                change_reason = raw_lesson["Substitution"]["TeacherAbsenceEffectName"]
        if raw_lesson["Substitution"]["Room"] is not None:
            room = raw_lesson["Substitution"]["Room"]["Code"]

    return {
        "lesson": lesson,
        "number": number,
        "start_time": start_time,
        "end_time": end_time,
        "display_time": start_time + " " + end_time,
        "room": room,
        "change": change,
        "change_reason": change_reason,
        "date": date,
    }


def process_data(raw_data: RawData) -> ProcessedLessons:
    processed_lessons: ProcessedLessons = []
    for raw_lesson in raw_data:
        processed_lessons.append(process_lesson(raw_lesson))
    return processed_lessons


def sort_lessons(unsorted_lessons: ProcessedLessons) -> Lessons:
    current_date = date.today()
    current_year, current_week, _ = current_date.isocalendar()
    sorted_lessons: Lessons = {
        "days": {"po": [], "wt": [], "sr": [], "cz": [], "pi": [], "so": [], "ni": []},
        "last_update": f"{current_year}-{current_week}",
    }

    for lesson in unsorted_lessons:
        sorted_lessons["days"][get_weekday(lesson["date"])].append(lesson)

    return sorted_lessons


def save_lessons(lessons: Lessons):
    with open("lessons.json", "w") as file:
        json.dump(lessons, file)


def updateData(week: int = 0):
    os.system(f"cd js_stuff && node main.js {week}")
    save_lessons(sort_lessons(process_data(load_data())))


if __name__ == "__main__":
    week: int = int(sys.argv[1])
    updateData(week)
