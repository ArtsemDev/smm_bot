from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

bot = Bot(
    token='5734659112:AAE8I8nH2ZKALeaCF2gdeYimqEJMVTS0tZY',
    # token=getenv('BOT_TOKEN'),
    parse_mode='Markdown'
)
dp = Dispatcher(name='dp')
