import asyncio
import logging
from urllib.parse import urlparse

import aiogram
from aiogram.exceptions import TelegramAPIError
from django.core.management.base import BaseCommand
from config import settings

# Set up logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Set or update the Telegram bot webhook."

    def handle(self, *args, **kwargs):
        """
        Execute the command to set the Telegram bot webhook.
        """
        # Log the webhook URL being used
        self.stdout.write(f"Setting webhook to: {settings.BOT_WEBHOOK_URL}")
        logger.info(f"Starting webhook setup for URL: {settings.BOT_WEBHOOK_URL}")

        # Validate the webhook URL
        if not self._is_valid_url(settings.BOT_WEBHOOK_URL):
            self.stdout.write(self.style.ERROR("Invalid webhook URL provided."))
            logger.error("Webhook URL is invalid.")
            return

        # Run the async webhook management
        try:
            asyncio.run(self.manage_webhook())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to set webhook: {str(e)}"))
            logger.exception("Webhook setup failed.")

    async def manage_webhook(self):
        """
        Manage the Telegram bot webhook by checking and setting it if necessary.
        """
        bot = aiogram.Bot(token=settings.BOT_TOKEN)

        try:
            # Get current webhook info
            webhook_info = await bot.get_webhook_info()
            self.stdout.write(f"Current webhook info: {webhook_info}")
            logger.info(f"Current webhook: {webhook_info.url}")

            # Set webhook if it differs from the desired URL
            if webhook_info.url != settings.BOT_WEBHOOK_URL:
                await bot.set_webhook(url=settings.BOT_WEBHOOK_URL)
                self.stdout.write(self.style.SUCCESS(f"Webhook set to: {settings.BOT_WEBHOOK_URL}"))
                logger.info(f"Webhook updated to: {settings.BOT_WEBHOOK_URL}")
            else:
                self.stdout.write("Webhook URL is already set to the desired value.")
                logger.info("Webhook URL already matches the desired value.")
        except TelegramAPIError as e:
            self.stdout.write(self.style.ERROR(f"Telegram API error: {str(e)}"))
            logger.error(f"Telegram API error during webhook setup: {str(e)}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
            logger.error(f"Unexpected error during webhook setup: {str(e)}")
        finally:
            await bot.session.close()
            logger.info("Bot session closed.")

    def _is_valid_url(self, url):
        """
        Validate that the provided URL is well-formed.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
