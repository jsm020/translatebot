# import io
# import aiohttp
# import easyocr
# from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Command
# from aiogram.types import ContentTypes
# from aiogram.types import InputFile
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from googletrans import Translator

# from data import config
# from loader import dp, bot, db
# reader = easyocr.Reader(['en'],gpu=False)

# @dp.message_handler(content_types=ContentTypes.PHOTO)
# async def start_ocr(message: types.Message):
#     await message.reply("Processing the image...")

#     # Get the photo with the highest resolution
#     file_id = message.photo[-1].file_id
#     photo_info = await bot.get_file(file_id)
#     photo_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{photo_info.file_path}"
#     print(photo_url)
#     text_result = reader.readtext(photo_url)
#     if text_result:
#         result_text = "\n".join([result[1] for result in text_result])


#         translator = Translator()
#         lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
#         lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)

#         translation = translator.translate(result_text, src=lang1, dest=lang2)
#         translate_text = translation.text

#         await message.answer(translate_text)
#     else:
#         await message.reply("Rasmdan text topilmadi")
