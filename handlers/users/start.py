import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.filters import language_callback_data, get_language_from_callback
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.mainkeyboard import create_menu_markup
from keyboards.inline.languageKeyboard import language1





@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username,
                                 choose_lan_1="Auto",
                                 choose_lan_2=message.from_user.language_code,)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    x = await create_menu_markup(message.from_user.id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali')

    await message.answer("Xush kelibsiz!", reply_markup=x)

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)


@dp.message_handler(lambda message: message.text in language_callback_data.keys())
async def update(message: types.Message):
    await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language1)
@dp.message_handler(text="🔁")
async def bot_start(message: types.Message):
    data = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    if data == "Auto":
        await message.answer("🔎 Avtomatik aniqlash da tilni alishtrib bulmaydi")
    else:
        await db.update_choice(telegram_id=message.from_user.id)
        x = await create_menu_markup(message.from_user.id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali')
        await message.answer("Til muvafaqqiyatli uzgardi", reply_markup=x)


@dp.message_handler(text="🎙 Ovoz orqali")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text='Text orqali', button2_text='🏞 Rasm orqali')
    await message.answer(f"Siz ovoz orqali tarjima qilishni tanladingiz.", reply_markup=x)


@dp.message_handler(text="Text orqali")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text="🎙 Ovoz orqali", button2_text='🏞 Rasm orqali')

    await message.answer(f"Siz text orqali tarjima qilishni tanladingiz ", reply_markup=x)


@dp.message_handler(text="🏞 Rasm orqali")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text="🎙 Ovoz orqali", button2_text="Text orqali")

    await message.answer(f"Siz rasm orqali tarjima qilishni tanladingiz ", reply_markup=x)
