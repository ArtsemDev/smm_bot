from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.models import QuestionAnswer


async def questions_panel_ikb(question_id: int):
    answers = await QuestionAnswer.all(question_id=question_id)
    buttons = [
        [
            InlineKeyboardButton(
                text=answer.answer,
                callback_data=f'{question_id}:{answer.id}'
            )
        ]
        for answer in answers
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
