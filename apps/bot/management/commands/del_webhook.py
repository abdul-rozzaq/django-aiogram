import asyncio
import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError
from django.core.management.base import BaseCommand
from config import settings

# Set up logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete the Telegram bot webhook and clear pending updates."

    def handle(self, *args, **kwargs):
        """
        Execute the command to delete the bot's webhook and clear pending updates.
        """
        self.stdout.write("Starting webhook deletion and clearing pending updates...")
        logger.info("Initiating webhook deletion process.")
        try:
            asyncio.run(self.clear_cache())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to clear webhook: {str(e)}"))
            logger.exception("Webhook deletion failed.")

    async def clear_cache(self):
        """
        Delete the existing Telegram webhook and drop any pending updates.
        """
        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))  # Optional, can be removed if not needed

        try:
            # Get current webhook info
            webhook_info = await bot.get_webhook_info()
            self.stdout.write(f"Current webhook info: {webhook_info}")
            logger.info(f"Current webhook: {webhook_info.url}")

            # Delete webhook if it exists
            if webhook_info.url:
                await bot.delete_webhook(drop_pending_updates=True)
                self.stdout.write(self.style.SUCCESS("Webhook deleted and pending updates cleared."))
                logger.info("Webhook deleted and pending updates dropped.")
            else:
                self.stdout.write("No webhook is currently set.")
                logger.info("No existing webhook found.")
        except TelegramAPIError as e:
            self.stdout.write(self.style.ERROR(f"Telegram API error: {str(e)}"))
            logger.error(f"Telegram API error during webhook deletion: {str(e)}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
            logger.error(f"Unexpected error during webhook deletion: {str(e)}")
        finally:
            await bot.session.close()
            self.stdout.write("Bot session closed.")
            logger.info("Bot session closed.")
