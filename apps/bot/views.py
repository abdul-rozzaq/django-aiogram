import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.bot.bot import feed_update
from config import settings


logger = logging.getLogger(__name__)


@csrf_exempt
async def handle_updates(request, bot_id: str):
    """
    Handle webhook updates
    """
    if not bot_id:
        return JsonResponse({"detail": "Bot ID is required"}, status=400)

    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if bot_id != settings.BOT_TOKEN.split(":", maxsplit=1)[0]:
        return JsonResponse({"detail": "Bot ID is not valid"}, status=400)

    update = request.body.decode("utf-8")

    try:
        update_data = json.loads(update)
        await feed_update(update=update_data)
        return JsonResponse({"status": "ok"})

    except Exception as exc:
        logger.error("Error handling webhook: %s", exc)
        return JsonResponse({"status": "ok"})
        # return JsonResponse({"status": "error", "error": str(exc)}, status=500)
