from django.urls import path
from .views import handle_updates

urlpatterns = [
    path("webhook/<str:bot_id>/updates/", handle_updates),
]
