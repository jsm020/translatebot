import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.filters import language_callback_data, get_language_from_callback, topish_til_kodi
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.mainkeyboard import create_menu_markup
from keyboards.inline.languageKeyboard import language1
from keyboards.inline.languagekeyboard2 import language2
from states.statedata import ChangeData, ChangeData2
from aiogram.dispatcher import FSMContext
from googletrans import Translator


# @dp.message_handler()
# async def translate_to_uzbek(message: types.Message):
#     try:
#         translator = Translator()
#         text = message.text
#         lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
#         lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)

#         print(f"Lang1: {lang1}, Lang2: {lang2}")  # Check retrieved languages

#         if lang1 is not None and lang2 is not None:
#             translated = translator.translate(text, src=lang1, dest=lang2)
#             print(translated)  # Check the translated text
#         else:
#             print("Language codes are None.")

#     except Exception as e:
#         print(f"An error occurred: {e}")  # Log any exceptions




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








@dp.message_handler(text="🔁",state="*")
async def bot_start(message: types.Message):
    data = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    if data == "Auto":
        await message.answer("🔎 Avtomatik aniqlash da tilni alishtrib bulmaydi")
    else:
        await db.update_choice(telegram_id=message.from_user.id)
        x = await create_menu_markup(message.from_user.id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali')
        await message.answer("Til muvafaqqiyatli uzgardi", reply_markup=x)


@dp.message_handler(text="🎙 Ovoz orqali", state="*")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text='Text orqali', button2_text='🏞 Rasm orqali')
    await message.answer(f"Siz ovoz orqali tarjima qilishni tanladingiz.", reply_markup=x)


@dp.message_handler(text="Text orqali", state="*")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text="🎙 Ovoz orqali", button2_text='🏞 Rasm orqali')

    await message.answer(f"Siz text orqali tarjima qilishni tanladingiz ", reply_markup=x)


@dp.message_handler(text="🏞 Rasm orqali", state="*")
async def bot_start(message: types.Message):
    x = await create_menu_markup(message.from_user.id, button1_text="🎙 Ovoz orqali", button2_text="Text orqali")

    await message.answer(f"Siz rasm orqali tarjima qilishni tanladingiz ", reply_markup=x)


@dp.message_handler(lambda message: message.text in language_callback_data.keys() ,state="*")
async def update(message: types.Message):
    # await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language1)
    text = message.text
    text = topish_til_kodi(text)    
    # print(text)
    data = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    # print(data)
    data2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
    # print(data2)
    if text == data:
        await ChangeData.lang1.set()
        await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language1)
    elif text ==data2:
        await ChangeData2.lang2.set()
        await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language2)
    


@dp.callback_query_handler(lambda call: call.data in language_callback_data.values(), state=ChangeData.lang1)
async def change_lan(call:types.CallbackQuery, state: FSMContext):
    text = call.data
    await db.update_user_choose_lan_1(telegram_id=call.from_user.id, choose_lan_1=text)
    x = await create_menu_markup(call.from_user.id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali')
    await call.message.answer("Til muvaqqiyatli uzgardi",reply_markup=x )
    await call.message.delete()
    await call.answer(cache_time=10)
    await state.finish()




@dp.callback_query_handler(lambda call: call.data in language_callback_data.values(), state=ChangeData2.lang2)
async def change_lan2(call:types.CallbackQuery, state: FSMContext):
    text = call.data
    await db.update_user_choose_lan_2(telegram_id=call.from_user.id, choose_lan_2=text)
    x = await create_menu_markup(call.from_user.id, button1_text='🎙 Ovoz orqali', button2_text='🏞 Rasm orqali')
    await call.message.answer("Til muvaqqiyatli uzgardi",reply_markup=x )
    await call.message.delete()
    await call.answer(cache_time=10)
    await state.finish()




