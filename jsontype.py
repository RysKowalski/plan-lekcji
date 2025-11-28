from typing import TypedDict, Optional


class DateInfo(TypedDict):
    """Represents a date with timestamp and display formats."""

    Timestamp: int
    Date: str
    DateDisplay: str
    Time: str


class Room(TypedDict):
    Id: int
    Code: str


class TimeSlot(TypedDict):
    Id: int
    Start: str
    End: str
    Display: str
    Position: int


class Subject(TypedDict):
    Id: int
    Key: str
    Name: str
    Kod: str
    Position: int


class Teacher(TypedDict):
    Id: int
    Surname: str
    Name: str
    DisplayName: str


class Change(TypedDict):
    Id: int
    Type: int
    IsMerge: bool
    Separation: bool


class Clazz(TypedDict):
    Id: int
    Key: str
    DisplayName: str
    Symbol: str


class Distribution(TypedDict):
    Id: int
    Key: str
    Shortcut: str
    Name: str
    PartType: str


class Substitution(TypedDict):
    Id: int
    UnitId: int
    ScheduleId: int
    LessonDate: DateInfo
    DateAt: str
    ChangeDate: Optional[str]
    ChangeDateAt: Optional[str]
    PupilNote: Optional[str]
    Reason: Optional[str]
    Event: Optional[str]
    Room: Optional[Room]
    TimeSlot: Optional[TimeSlot]
    Subject: Optional[Subject]
    TeacherPrimary: Optional[Teacher]
    TeacherAbsenceReasonId: Optional[int]
    TeacherAbsenceEffectName: str
    TeacherSecondary: Optional[Teacher]
    TeacherSecondaryAbsenceReasonId: Optional[int]
    TeacherSecondaryAbsenceEffectName: Optional[str]
    TeacherSecondary2: Optional[Teacher]
    TeacherSecondary2AbsenceReasonId: Optional[int]
    TeacherSecondary2AbsenceEffectName: Optional[str]
    Change: Change
    Clazz: Clazz
    Distribution: Distribution
    ClassAbsence: bool
    NoRoom: bool
    DateModified: DateInfo
    ModifiedAt: str
    Description: Optional[str]


class SingleLesson(TypedDict):
    Id: int
    MergeChangeId: Optional[int]
    Event: Optional[str]
    Date: DateInfo
    DateAt: str
    Room: Optional[Room]
    TimeSlot: TimeSlot
    Subject: Subject
    TeacherPrimary: Teacher
    TeacherSecondary: Optional[Teacher]
    TeacherSecondary2: Optional[Teacher]
    Change: Optional[Change]
    Clazz: Clazz
    Distribution: Distribution
    PupilAlias: Optional[str]
    Visible: bool
    Substitution: Substitution
    Parent: Optional[str]


class SingleProcessedLesson(TypedDict):
    """
    lesson: 2 letters
    number: lesson number in day
    start_time: HH:MM
    end_time: HH:MM
    display_time: HH:MM-HH:MM
    room: 2 letter class code, default 00
    change: 0: no change; 1: substitution; 2: deleted; 3: moved
    change_reason: str
    date: RRRR-MM-DD
    """

    lesson: str  # 2 letters
    number: int
    start_time: str
    end_time: str
    display_time: str
    room: str
    change: int
    change_reason: str
    date: str


ProcessedLessons = list[SingleProcessedLesson]


class Colors(TypedDict):
    base: str
    naglowek: str
    number: str
    time: str
    lesson: str
    room: str


class SortedProcessedLessons(TypedDict):
    po: ProcessedLessons
    wt: ProcessedLessons
    sr: ProcessedLessons
    cz: ProcessedLessons
    pi: ProcessedLessons


class Lessons(TypedDict):
    days: SortedProcessedLessons
    last_update: str


RawData = list[SingleLesson]
