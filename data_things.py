import json
from jsontype import RawData, SingleLesson, ProcessedLessons, SingleProcessedLesson


def load_data() -> RawData:
    with open("raw.json", "r") as file:
        data: RawData = json.load(file)
    return data


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
        lesson = raw_lesson["Subject"]["Kod"]
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
        processed_lesson = process_lesson(raw_lesson)
    return processed_lessons


if __name__ == "__main__":
    data: RawData = load_data()
    print(json.dumps(process_data(data)))
