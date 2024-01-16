from django.shortcuts import render, redirect
from .models import Room, Message
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

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        'user':username,
        'room_name':room_name,
        'messages':get_messages,
    }
    return render(request, 'message.html', context)