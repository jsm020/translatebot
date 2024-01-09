import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.mainkeyboard import menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username,
                                 choose_lan_1=message.from_user.language_code,
                                 choose_lan_2="Auto")
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    data1 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
    data2 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)

    print(data1, data2)

    menu.keyboard[0][0].text = data1
    menu.keyboard[0][2].text = data2



    await message.answer("Xush kelibsiz!", reply_markup=menu)

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)


@dp.message_handler()
async def update(message: types.Message):
    update_data = await db.update_user_choose_lan_1(message=message.from_user.id,
                                                    choose_lan_1=message.text)
