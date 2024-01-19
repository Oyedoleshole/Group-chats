from django.shortcuts import render, redirect
from .models import Room, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def CreateRoom(request):
    if request.method == "POST":
        username = request.POST['username']
        room = request.POST['room']
        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room',room_name=room, username=username)
        except:
            new_room = Room(room_name=room)
            new_room.save()
    return render(request, 'index.html')

@login_required(login_url='create-room')
def chat_with(request):
    all_user = User.objects.all()
    return render(request, "chat_with.html",{'all_user':all_user})


def connect_with(request, user, join_user):
    get_user = user
    get_join_user = join_user
    return render(request, 'chat_screen.html',{'user':get_user,'joinee_user':get_join_user})

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        'user':username,
        'room_name':room_name,
        'messages':get_messages,
    }
    return render(request, 'message.html', context)