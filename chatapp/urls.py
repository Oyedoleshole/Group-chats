from django.urls import path
from . import views
from .consumers import ChatConsumer

urlpatterns = [
    path('',views.CreateRoom, name='create-room'),
    path('<str:room_name>/<str:username>',views.MessageView, name='room'),
    # path('ws/notification/<str:room_name/',ChatConsumer.as_asgi())
]