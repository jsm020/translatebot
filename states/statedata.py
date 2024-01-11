from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangeData(StatesGroup):
    lang1 = State()


class ChangeData2(StatesGroup):
    lang2 = State()



class OvozAniqlash(StatesGroup):
    ovoz_aniqlash= State()



class TextAniqlash(StatesGroup):
    text_aniqlash= State()


class RasmAniqlash(StatesGroup):
    rasm_aniqlash= State()


class kiril_latin(StatesGroup):
    kirllatin= State()