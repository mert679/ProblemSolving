from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Room, MessageRoom, DrawingData
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ImageUploadForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

def index(request):
    return render(request, "main_page.html")
def how_it_works(request):
    return render(request, "how_it_works.html")
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        try:
            if password == password2:
                user = User.objects.create_user(username,email,password)
                user.save()
                return render(request, "signup.html", {
                    "message": "Your account has been successfully created."
                })
            
            else:
                  return render(request, "signup.html", {
                    "message": "Passwords do not match."
                })
        except IntegrityError:
            return render(request,"signup.html",{
                "message": "Username already taken."
            })
    return render(request,"signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        psw = request.POST["password"]

        user = authenticate(request,username=username,password=psw)

        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            return render( request,"login.html",{
                "message":"Invalid username and/or password."
            })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))
# Home Page After User login

@login_required
def HomePageView(request):
    room = Room.objects.all()
    room_ids = list(room.values_list('id', flat=True)) 
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        
            return redirect('/home')
    else:
        form = ImageUploadForm()
    return render(request,"room_list_page.html",{'form': form, "rooms":room, 'room_ids': room_ids})

@login_required
def room_detail(request,id):
    room = Room.objects.get(id=id)
    remaining_time = room.remaining_time()
    
    if room.can_join():
        room.users.add(request.user)
        messages = MessageRoom.objects.filter(room=room)[0:20]
        drawing_data = DrawingData.objects.filter(room=room)[0:1000]
        # if remaining_time.total_seconds() <= 0:
        # # If remaining time is 0 or negative, delete the room
        #     room.delete()
        #     return redirect('/home')
        
        return render(request, "room_detail_page.html",{'room':room, 'messages':messages,"time_remaining":remaining_time,"drawing_data":drawing_data})
    else:
        return HttpResponseForbidden("Room is full")

@login_required
def ProfilePageView(request):
    user = request.user  # Get the current user
    if request.method == "POST":
        user.username = request.POST.get("u_username", user.username)
        user.email = request.POST.get("u_email", user.email)
        password = request.POST.get("u_password")
        password2 = request.POST.get("u_password2")
        if password and password == password2:
            user.set_password(password)
            user.save()
            return redirect('/login/')
            
        else:
                return render(request, "user_profile_page.html", {
                    "message": "Passwords do not match."
                }) 
    return render(request, "user_profile_page.html", {'user': user})

@login_required
def whiteboard_empty(request):
    return render(request,"new_empty_whiteboard.html")