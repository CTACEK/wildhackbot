from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Новая заявка"),
        ],
        [
            KeyboardButton(text="FAQ"),
            KeyboardButton(text="О заповеднике")
        ],
    ],
    resize_keyboard=True
)