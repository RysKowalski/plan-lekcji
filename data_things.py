import json
from jsontype import RawData, SingleLesson, ProcessedLessons, SingleProcessedLesson


def load_data() -> RawData:
    with open("raw.json", "r") as file:
        data: RawData = json.load(file)
    return data


def process_lesson(raw_lesson: SingleLesson, number: int) -> SingleProcessedLesson:
    change: int = 0
    if raw_lesson["Change"] is not None:
        change = 1

    lesson: str = "None"
    start_time: str = "01:01"
    end_time: str = "01:02"
    display_time: str = "01:01-01:02"
    room: str = "00"

    if change == 0:
        lesson = raw_lesson["Subject"]["Kod"]
        start_time = raw_lesson["TimeSlot"]["Start"]
        end_time = raw_lesson["TimeSlot"]["End"]
        display_time = raw_lesson["TimeSlot"]["Display"]
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
    }


def process_data(raw_data: RawData) -> ProcessedLessons:
    processed_lessons: ProcessedLessons = []
    for i, raw_lesson in enumerate(raw_data):
        processed_lessons.append(process_lesson(raw_lesson, i))
    return processed_lessons


if __name__ == "__main__":
    data: RawData = load_data()
    print(json.dumps(process_data(data)))
