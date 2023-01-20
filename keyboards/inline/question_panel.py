from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.models import QuestionAnswer


class QuestionCallbackData(CallbackData, prefix='question'):
    question_id: int = None
    answer_id: int = None


async def questions_panel_ikb(question_id: int):
    answers = await QuestionAnswer.all(question_id=question_id)
    buttons = [
        [
            InlineKeyboardButton(
                text=answer.answer,
                callback_data=QuestionCallbackData(
                    question_id=question_id,
                    answer_id=answer.id
                ).pack()
            )
        ]
        for answer in answers
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
