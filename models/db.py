from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Users:
    id: int
    telegram_id: int
    user_name: str
    name: str
    surname: str
    registered_at: datetime
    role: str


@dataclass(frozen=True)
class Statistics:
    id: int
    user_id: int
    test_id: int
    score: int
    solved_at: datetime


@dataclass(frozen=True)
class Subjects:
    id: int
    name: str
    description: str


@dataclass(frozen=True)
class Topics:
    id: int
    text: str
    subject_id: int


@dataclass(frozen=True)
class Tests:
    id: int
    created_at: datetime
    topic_id: int


@dataclass(frozen=True)
class Questions:
    id: int
    test_id: int
    text: str
    created_at: datetime


@dataclass(frozen=True)
class Answers:
    id: int
    question_id: int
    text: str
    created_at: datetime
    is_correct: int
