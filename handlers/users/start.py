import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.filters import language_callback_data, get_language_from_callback, topish_til_kodi
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.mainkeyboard import create_menu_markup
from keyboards.inline.languageKeyboard import language1
from keyboards.inline.languagekeyboard2 import language2
from states.statedata import ChangeData, ChangeData2, OvozAniqlash
from aiogram.dispatcher import FSMContext
from googletrans import Translator
import os
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
from loader import dp, bot, db
import speech_recognition as sr













###########################33
@dp.message_handler(CommandStart(), state="*")
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



# Assuming `dp` is your Dispatcher instance


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
    await OvozAniqlash.ovoz_aniqlash.set()







@dp.message_handler(content_types=types.ContentType.VOICE, state=OvozAniqlash.ovoz_aniqlash)
async def handle_voice_message(message: types.Message, state: FSMContext):
    voice_file = await message.voice.get_file()
    file_extension = voice_file.file_path.split('.')[-1]
    file_name = f"voice/voice_{message.message_id}.{file_extension}"
    await bot.download_file(voice_file.file_path, file_name)
    converted_file_name = "voice/converted.wav"
    os.system(f"ffmpeg -i {file_name} {converted_file_name}")
    audio = AudioSegment.from_file(converted_file_name, format="wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile(converted_file_name) as source:
        audio = recognizer.record(source)
    try:
        lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
        lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
        transcribed_text = recognizer.recognize_google(audio, language=lang1)
        translator = Translator()

        translation = translator.translate(transcribed_text, src=lang1, dest=lang2)
        translate_text = translation.text

        await message.answer(translate_text)

    except sr.UnknownValueError:
        await message.reply("Ovoz topilmadi.")
    except sr.RequestError as e:
        await message.reply(f"Произошла ошибка при обработке голосового сообщения: {e}")

    # Удаляем звуковые файлы
    os.remove(file_name)
    os.remove(converted_file_name)



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





@dp.message_handler(lambda message: message.text not in language_callback_data.keys() if language_callback_data else True)
async def translate_text(message: types.Message):
    translator = Translator()
    lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)

    translation = translator.translate(message.text, src=lang1, dest=lang2)
    translate_text = translation.text

    await message.answer(translate_text)