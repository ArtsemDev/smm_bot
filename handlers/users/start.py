from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from utils.models import User
from keyboards.inline import questions_panel_ikb

start_router = Router(name='start')


@start_router.message(CommandStart())
async def command_start(message: Message):
    await message.delete()
    user = User(id=message.from_user.id)
    try:
        await user.save()
    except IntegrityError:
        text = f'Давно не виделись! {message.from_user.full_name}'
    else:
        text = f'Привет, новый друг {message.from_user.full_name}'
    await message.answer(
        text=text,
        reply_markup=await questions_panel_ikb(question_id=1)
    )


@start_router.message(F.text == 'HELLO!')
async def hello_message(message: Message):
    await message.delete()
    await message.answer(
        text='GOODBYE!'
    )


@start_router.message()
async def echo(message: Message):
    await message.delete()
