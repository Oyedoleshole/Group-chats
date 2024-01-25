from django.urls import path, include
from . import views
from django_private_chat import urls as django_private_chat_urls
from .agora_config import get_token

urlpatterns = [
    path('login',views.login_user,name='login'),
    path('',views.CreateRoom, name='create-room'),
    path('<str:room_name>/<str:username>',views.MessageView, name='room'),
    path('private_chat', include('django_private_chat.urls')),
    path('chat-with/',views.chat_with,name='chat-with'),
    path('connection/<str:user>/<str:join_user>',views.connect_with, name='connect_with_'),
    path('video_room/',views.video_room),
    path('video_room_enter/',views.video_room_enter),
    path('get_token/',get_token),
    path('createUser/',views.createUser),
    path('getUser/',views.getUser),
]