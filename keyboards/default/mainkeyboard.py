from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.filters import get_language_from_callback
from loader import db
async def get_choose_lan_1(telegram_id):
    choose_lan_1 = await db.select_user_choose_lan_1(telegram_id) 
    return choose_lan_1
async def get_choose_lan_2(telegram_id):
    choose_lan_2 = await db.select_user_choose_lan_2(telegram_id) 
    return choose_lan_2
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def create_menu_markup(telegram_id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali'):
    choose_lan_1 = await get_choose_lan_1(telegram_id)
    choose_lan_1 = get_language_from_callback(choose_lan_1)

    choose_lan_2 = await get_choose_lan_2(telegram_id)
    choose_lan_2 = get_language_from_callback(choose_lan_2)

    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=choose_lan_1),
                KeyboardButton(text='🔁'),
                KeyboardButton(text=choose_lan_2),
            ],
            [
                KeyboardButton(text=button1_text),  # You can now pass custom text for this button
                KeyboardButton(text='Kiril_Lotin'),
                KeyboardButton(text=button2_text),  # You can now pass custom text for this button
            ]
        ],
        resize_keyboard=True
    )

    return menu

