# import os
# from googletrans import Translator
# import speech_recognition as sr
# from pydub import AudioSegment
# from loader import dp, bot, db
# import speech_recognition as sr


# @dp.message_handler(content_types=types.ContentType.VOICE)
# async def handle_voice_message(message: types.Message):
#     voice_file = await message.voice.get_file()
#     file_extension = voice_file.file_path.split('.')[-1]
#     file_name = f"voice/voice_{message.message_id}.{file_extension}"
#     await bot.download_file(voice_file.file_path, file_name)
#     converted_file_name = "voice/converted.wav"
#     os.system(f"ffmpeg -i {file_name} {converted_file_name}")
#     audio = AudioSegment.from_file(converted_file_name, format="wav")
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(converted_file_name) as source:
#         audio = recognizer.record(source)
#     try:
#         lang1 = await db.select_user_choose_lan_1(telegram_id=message.from_user.id)
#         lang2 = await db.select_user_choose_lan_2(telegram_id=message.from_user.id)
#         transcribed_text = recognizer.recognize_google(audio, language=lang1)
#         translator = Translator()

#         translation = translator.translate(transcribed_text, src=lang1, dest=lang2)
#         translate_text = translation.text

#         await message.answer(translate_text)

#     except sr.UnknownValueError:
#         await message.reply("Ovoz topilmadi.")
#     except sr.RequestError as e:
#         await message.reply(f"Произошла ошибка при обработке голосового сообщения: {e}")

#     # Удаляем звуковые файлы
#     os.remove(file_name)
#     os.remove(converted_file_name)



