from aiogram import Bot, Dispatcher, types
from django.conf import settings

from apps.bot.handlers.user import router


webhook_dp = Dispatcher()
webhook_dp.include_router(router=router)


async def feed_update(update: dict):
    try:
        webhook_book = Bot(token=settings.BOT_TOKEN)
        aiogram_update = types.Update(**update)
        await webhook_dp.feed_update(bot=webhook_book, update=aiogram_update)
    finally:
        await webhook_book.session.close()
