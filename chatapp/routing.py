from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import ChatConsumer, Privatechat

websocket_urlspatterns = [
    path('ws/notification/<str:room_name>/<str:user>/', ChatConsumer.as_asgi()),
    path('ws/private-chat/<str:user>/<str:joinee_user>/',Privatechat.as_asgi())
]

# application = ProtocolTypeRouter({
#     "websocket": URLRouter(
#         websocket_urlspatterns
#     ),
# })
