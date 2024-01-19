from django.urls import path, include
from . import views
from django_private_chat import urls as django_private_chat_urls

urlpatterns = [
    path('',views.CreateRoom, name='create-room'),
    path('<str:room_name>/<str:username>',views.MessageView, name='room'),
    path('private_chat', include('django_private_chat.urls')),
    path('chat-with/',views.chat_with),
    path('connection/<str:user>/<str:join_user>',views.connect_with, name='connect_with_')
]