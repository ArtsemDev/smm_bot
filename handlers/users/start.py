from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from keyboards.inline import questions_panel_ikb
from utils.models import User, Question

start_router = Router(name='start')


@start_router.message(CommandStart())
async def command_start(message: Message):
    await message.delete()
    user = User(id=message.from_user.id)
    try:
        await user.save()
    except IntegrityError:
        pass
    question = await Question.all(limit=1)
    if question:
        await message.answer(
            text=question[0].question,
            reply_markup=await questions_panel_ikb(question_id=question[0].id)
        )


# @start_router.message(F.text == 'HELLO!')
# async def hello_message(message: Message):
#     await message.delete()
#     await message.answer(
#         text='GOODBYE!'
#     )


@start_router.message()
async def echo(message: Message):
    await message.delete()
