from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import ChatConsumer

websocket_urlspatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi())
]

# application = ProtocolTypeRouter({
#     "websocket": URLRouter(
#         websocket_urlspatterns
#     ),
# })
