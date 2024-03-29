language_callback_data = {
    "🔎 Avtomatik aniqlash": "Auto",
    "Rus 🇷🇺": "ru",
    "Ingliz 🇬🇧": "en",
    "Qozoq 🇰🇿": "kk",
    "O'zbek 🇺🇿": "uz",
    "Frantsuz 🇫🇷": "fr",
    "Tojik 🇹🇯": "tg",
    # "Turkman 🇹🇲": "tk",
    "Qirg'iz 🇰🇬": "ky",
    "Ispancha 🇪🇸": "es",
    "Belarus 🇧🇾": "be",
    "Ukrain 🇺🇦": "uk",
    "Arman 🇦🇲": "hy",
    "Nemis 🇩🇪": "de",
    "Italyan 🇮🇹": "it",
    "Fors 🇮🇷": "fa",
    "Turk 🇹🇷": "tr",
    "Koreys 🇰🇷": "ko",
    "Arabcha 🇸🇦": "ar",
    "Yapon 🇯🇵": "ja",
    "Xitoy(oddiy) 🇨🇳": "zh-cn",
    "Xitoy(A`nanaviy) 🇨🇳": "zh-tw"
} 

def get_language_from_callback(callback):
    return next((language for language, cb_data in language_callback_data.items() if cb_data == callback), None)




def topish_til_kodi(soz):
    return language_callback_data.get(soz)



