from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dispatcher import dp
from config import adminpass


class FMSAdmin(StatesGroup):
    temppass = State()
    connectionpass = State()


@dp.message_handler(commands="admin", state=None)
async def admin(message: types.Message, state: FSMContext):
    await FMSAdmin.temppass.set()
    await message.answer(f"Введите пароль от админа:")


@dp.message_handler(state=FMSAdmin.temppass)
async def admin(message: types.Message, state: FSMContext):
    if message.text == adminpass:
        await FMSAdmin.connectionpass.set()
        await message.answer(f"Введите пароль от админа:")



