from django.shortcuts import render, redirect
from .models import Room, Message
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "No User Found")
            return redirect('login')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('chat-with')
    return render(request, 'login.html')
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

@login_required(login_url='login')
def chat_with(request):
    all_user = User.objects.all()
    return render(request, "chat_with.html",{'all_user':all_user})


def connect_with(request, user, join_user):
    get_user = user
    get_join_user = join_user
    all_user = User.objects.all()
    return render(request, 'chat_screen.html',{'user':get_user,'joinee_user':get_join_user,'all_user':all_user})

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        'user':username,
        'room_name':room_name,
        'messages':get_messages,
    }
    return render(request, 'message.html', context)

def video_room(request):
    return render(request, 'room.html')

def video_room_enter(request):
    return render(request, 'lobby.html')
@csrf_exempt
def createUser(request):
    print(request.body)
    data = json.loads(request.body)
    member, create = Room.objects.get_or_create(
        room_name=data['room_name'],
        name=data['name'],
        uid=data['UID']
    )
    return JsonResponse({"name":data['name']},safe=False)

def getUser(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    users = Room.objects.get(room_name=room_name, uid=uid)
    return JsonResponse({"name":users.name},safe=False)