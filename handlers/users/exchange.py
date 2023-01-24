from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from utils.nominatim import NominatimAPI
from utils.exchange import BelarusbankAPI, BelAgroBankAPI

exchange_router = Router()


class ExchangeStatesGroup(StatesGroup):
    city = State()


@exchange_router.message(F.text == '/exchange')
async def get_exchange(message: Message, state: FSMContext = None):
    await state.set_state(ExchangeStatesGroup.city)
    await message.answer(
        text='Введите город или поделитесь геолокацией!',
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False,
            keyboard=[[KeyboardButton(
                text='ПОДЕЛИТЬСЯ ГОРОДОМ',
                request_location=True
            )]]
        )
    )


@exchange_router.message(ExchangeStatesGroup.city)
async def get_city(message: Message):
    response = await BelAgroBankAPI.get_exchange(
        ondate=datetime.today().strftime('%m/%d/%Y')
    )
    usd = list(
        filter(
            lambda x: x.get('CharCode') == 'USD',
            response.get('DailyExRates').get('Currency')
        )
    )[0]
    await message.answer(
        text=usd.get('RateBuy')
    )
    # if message.location:
    #     nominatim_response = await NominatimAPI.get_reverse(
    #         lat=message.location.latitude,
    #         lon=message.location.longitude
    #     )
    #     city = nominatim_response.get('address').get('city')
    # else:
    #     nominatim_response = await NominatimAPI.get_search(city=message.text.title())
    #     if nominatim_response:
    #         city = nominatim_response[0].get('display_name').split(',')[0]
    #     else:
    #         city = None
    # await message.answer(
    #     text=(
    #         await BelarusbankAPI.get_exchange(city=city)
    #     )[0].get('USD_in')
    # )
