import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import urllib3
from data import config
from data.filters import language_callback_data, get_language_from_callback, topish_til_kodi
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.mainkeyboard import create_menu_markup,atmenkeyboard
from keyboards.inline.languageKeyboard import language1
from keyboards.inline.languagekeyboard2 import language2
from states.statedata import ChangeData, ChangeData2,kiril_latin,Aniqlash
from aiogram.dispatcher import FSMContext
from googletrans import Translator
import os
import pytesseract
import urllib.request

from PIL import Image
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
from loader import dp, bot, db
import speech_recognition as sr
from data.transliterate import to_cyrillic, to_latin



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

    x = await create_menu_markup(message.from_user.id)

    await message.answer("Xush kelibsiz!", reply_markup=x)

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
    await Aniqlash.aniqlash.set()


@dp.message_handler(text="🔁",state=Aniqlash.aniqlash)
async def bot_start(message: types.Message):
    data = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    data2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
    if data == "Auto":
        await message.answer("🔎 Avtomatik aniqlash da tilni alishtrib bulmaydi")
    else:
        await db.update_choice(telegram_id=message.from_user.id)
        x = await create_menu_markup(message.from_user.id)
        await message.answer(f"✅ Til muvaffaqiyatli o'zgartirildi.\n\n{get_language_from_callback(data)}→{get_language_from_callback(data2)}",reply_markup=x )


@dp.message_handler(text="Kiril_Lotin", state=Aniqlash.aniqlash)
async def kiril_latin_tarjim(message:types.Message):
    await message.answer("Matn yuboring", reply_markup=atmenkeyboard)
    await kiril_latin.kirllatin.set()

@dp.message_handler(content_types=types.ContentType.VOICE, state="*")
async def handle_voice_message(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)

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




@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=Aniqlash.aniqlash)
async def start_ocr(message: types.Message):
    await message.reply("Text aniqlanmoqda...")
    file_id = message.photo[-1].file_id
    photo_info = await bot.get_file(file_id)
    photo_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{photo_info.file_path}"

    image_path = f"photo/photo_{message.message_id}"
    urllib.request.urlretrieve(photo_url, image_path)

    text_result = pytesseract.image_to_string(Image.open(image_path))

    if text_result:
        result_text = "\n".join(text_result.splitlines())

        translator = Translator()
        lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
        lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)

        translation = translator.translate(result_text, src=lang1, dest=lang2)
        translate_text = translation.text
        await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)

        await message.answer(translate_text)
        os.remove(image_path)
    else:
        await message.reply("Rasmdan text topilmadi")
        os.remove(image_path)





@dp.message_handler(lambda message: message.text in language_callback_data.keys() ,state=Aniqlash.aniqlash)
async def update(message: types.Message):
    text = message.text
    text = topish_til_kodi(text)    
    data = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    data2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
    if text == data:
        await ChangeData.lang1.set()
        await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language1)
    elif text ==data2:
        await ChangeData2.lang2.set()
        await message.answer("Qaysi tildan tarjima qilmoqchisiz? Tanlang: 🔻", reply_markup=language2)
    


@dp.callback_query_handler(text="atmen", state=[ChangeData.lang1,ChangeData2.lang2])
async def change(call:types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.finish()

@dp.callback_query_handler(lambda call: call.data in language_callback_data.values(), state=ChangeData.lang1)
async def change_lan(call:types.CallbackQuery, state: FSMContext):
    text = call.data
    lang1 = await db.select_user_choose_lan_1(telegram_id=call.from_user.id)
    lang2 = await db.select_user_choose_lan_2(telegram_id=call.from_user.id)

    if call.data == lang1 or call.data == lang2:
        await call.answer("Siz bu tilni tanlagansiz")
    else:
        await db.update_user_choose_lan_1(telegram_id=call.from_user.id, choose_lan_1=text)
        x = await create_menu_markup(call.from_user.id)
        await call.message.answer(f"✅ Til muvaffaqiyatli o'zgartirildi.\n\n{get_language_from_callback(lang1)}→{get_language_from_callback(text)}",reply_markup=x )
        await call.message.delete()
        await call.answer(cache_time=10)
        await state.finish()




@dp.callback_query_handler(lambda call: call.data in language_callback_data.values(), state=ChangeData2.lang2)
async def change_lan2(call:types.CallbackQuery, state: FSMContext):
    text = call.data
    lang1 = await db.select_user_choose_lan_1(telegram_id=call.from_user.id)
    lang2 = await db.select_user_choose_lan_2(telegram_id=call.from_user.id)

    if call.data == lang2 or call.data ==lang1:
        await call.answer("Siz bu tilni tanlagansiz")
        
    else:
        await db.update_user_choose_lan_2(telegram_id=call.from_user.id, choose_lan_2=text)
        x = await create_menu_markup(call.from_user.id)

        await call.message.answer(f"✅ Til muvaffaqiyatli o'zgartirildi.\n\n{get_language_from_callback(lang2)}→{get_language_from_callback(text)}",reply_markup=x )
        await call.message.delete()
        await call.answer(cache_time=10)
        await state.finish()

@dp.message_handler(text="Bekor qilish",state="*")
async def kirillatintarjima(message:types.Message, state:FSMContext):
    x = await create_menu_markup(message.from_user.id)
    await state.finish()
    await message.answer("Tarjima qilishingiz mumkin", reply_markup=x)

    await Aniqlash.aniqlash.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state=kiril_latin.kirllatin)
async def kirillatintarjim(message:types.Message, state:FSMContext):
    matn = message.text
    if matn.isascii():
        await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
        await message.answer(to_cyrillic(matn))
    else:
        await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
        await message.answer(to_latin(matn))




@dp.message_handler(lambda message: message.text not in language_callback_data.keys() if language_callback_data else True, state=Aniqlash.aniqlash)
async def translate_text(message: types.Message, state:FSMContext):
    translator = Translator()
    lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
    lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)

    translation = translator.translate(message.text, src=lang1, dest=lang2)
    translate_text = translation.text
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)

    await message.answer(translate_text)





