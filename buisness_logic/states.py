

from aiogram.fsm.state import State, StatesGroup

class TestState(StatesGroup):
    subject = State()
    chapter = State()
    topic = State()
    test = State()

class Testing(StatesGroup):
    question = State()
    answer = State()

