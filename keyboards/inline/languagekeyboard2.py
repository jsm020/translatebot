from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 1-usul.
language2 = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Rus 🇷🇺", callback_data="ru"),
        InlineKeyboardButton(text="Ingliz 🇬🇧", callback_data="en"),
    ],
    [
        InlineKeyboardButton(text="Qozoq 🇰🇿", callback_data="kk"),
        InlineKeyboardButton(text="O'zbek 🇺🇿", callback_data="uz"),
    ],
    [
        InlineKeyboardButton(text="Lotin 🇺🇿", callback_data="uz-Latn"),
        InlineKeyboardButton(text="Frantsuz 🇫🇷", callback_data="fr"),
    ],
    [
        InlineKeyboardButton(text="Tojik 🇹🇯", callback_data="tg"),
        InlineKeyboardButton(text="Turkman 🇹🇲", callback_data="tk"),
    ],
    [
        InlineKeyboardButton(text="Qirg'iz 🇰🇬", callback_data="ky"),
        InlineKeyboardButton(text="Ispancha 🇪🇸", callback_data="es"),
    ],
    [
        InlineKeyboardButton(text="Belarus 🇧🇾", callback_data="be"),
        InlineKeyboardButton(text="Ukrain 🇺🇦", callback_data="uk"),
    ],
    [
        InlineKeyboardButton(text="Arman 🇦🇲", callback_data="hy"),
        InlineKeyboardButton(text="Nemis 🇩🇪", callback_data="de"),
    ],
    [
        InlineKeyboardButton(text="Italyan 🇮🇹", callback_data="it"),
        InlineKeyboardButton(text="Fors 🇮🇷", callback_data="sv"),
    ],
    [
        InlineKeyboardButton(text="Turk 🇹🇷", callback_data="tr"),
        InlineKeyboardButton(text="Koreys 🇰🇷", callback_data="ko"),
    ],
    [
        InlineKeyboardButton(text="Arabcha 🇸🇦", callback_data="ar"),
        InlineKeyboardButton(text="Yapon 🇯🇵", callback_data="ja"),
    ],
    [
        InlineKeyboardButton(text="Xitoy(oddiy) 🇨🇳", callback_data="zh"),
        InlineKeyboardButton(text="Xitoy(A`nanaviy) 🇨🇳", callback_data="zh-Hant"),
    ],
])