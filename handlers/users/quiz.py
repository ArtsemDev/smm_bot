from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import questions_panel_ikb, QuestionCallbackData
from utils.models import Question, QuestionAnswer, Product

quiz_router = Router(name='quiz')


@quiz_router.callback_query(QuestionCallbackData.filter())
async def get_answer(callback: CallbackQuery, callback_data: QuestionCallbackData):
    answer = await QuestionAnswer.get(pk=callback_data.answer_id)
    if answer.next_question_id:
        question = await Question.get(pk=answer.next_question_id)
        await callback.message.edit_text(
            text=question.question,
            reply_markup=await questions_panel_ikb(question_id=question.id)
        )
    else:
        product = await Product.get(pk=answer.product_id)
        await callback.message.edit_text(
            text=product.name,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text='LINK',
                            url=product.url
                        )
                    ]
                ]
            ) if product.url else None
        )
