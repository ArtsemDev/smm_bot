from aiogram.fsm.state import StatesGroup, State


class QuizStatesGroup(StatesGroup):
    question = State()
