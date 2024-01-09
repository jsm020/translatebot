from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='🔎 Avtomatik aniqlash'),
            KeyboardButton(text='🔁'),
            KeyboardButton(text='Lotin 🇺🇿'),
        ],
        [
            KeyboardButton(text='🎙 Ovoz orqali'),
            KeyboardButton(text='🏞 Rasm orqali'),
        ]
    ],
    resize_keyboard=True
)