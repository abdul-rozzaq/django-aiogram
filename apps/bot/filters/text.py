from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class TextFilter(BaseFilter):
    """
    Text filter class responsible for filtering messages
    for given message text.
    """

    def __init__(self, text: str | list[str]):
        if isinstance(text, str):
            self.text = [text]
        else:
            self.text = text

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        if isinstance(obj, Message):
            txt = obj.text or obj.caption
            return any(i == txt for i in self.text)
        elif isinstance(obj, CallbackQuery):
            return obj.data in self.text


class StartsWithFilter(BaseFilter):
    """
    StartsWith filter class for filtering messages or callback queries
    that start with a specific prefix.
    """

    def __init__(self, prefix: str | list[str]):
        if isinstance(prefix, str):
            self.prefix = [prefix]
        else:
            self.prefix = prefix

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        if isinstance(obj, Message):
            txt = obj.text or obj.caption
            return any(txt.startswith(p) for p in self.prefix if txt)
        elif isinstance(obj, CallbackQuery):
            return any(obj.data.startswith(p) for p in self.prefix if obj.data)
