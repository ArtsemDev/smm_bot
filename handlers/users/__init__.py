from aiogram import Router

from .start import start_router
from .quiz import quiz_router

user_router = Router(name='users')
user_router.include_router(start_router)
user_router.include_router(quiz_router)


__all__ = ['user_router']
