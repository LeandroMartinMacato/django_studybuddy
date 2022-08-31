from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room , Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id' : 1, 'name' : "Lets Learn Python"},
#     {'id' : 2, 'name' : "Design with me"},
#     {'id' : 3, 'name' : "Frontend developers"},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request , "User doesn't exist")

        user = authenticate(request , username = username, password = password)

        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , "Username or Password does not exist")

    context = {'page' : page}
    return render(request , 'base/login_register.html' , context)

def logoutUser(request):
    logout(request) # delete session cookies from session
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # to get user object
            user.username = user.username.lower() # to standardize username to lowercase
            user.save()
            login(request , user) # login the user after register
            return redirect('home')
        else:
            messages.error(request , 'an error occurred during registration')

    context = {'page' : page , 'form' : form}
    return render(request , 'base/login_register.html' , context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' #get the '?q=[QUERY]'

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    ) # all in db
    room_count = rooms.count()

    topic = Topic.objects.all() # get all topic from db

    context = {'rooms' : rooms , 'topics' : topic , 'room_count' : room_count}
    return render(request , 'base/home.html' , context ) 

def room(request , pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request , 'base/room.html' , context ) 

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # if there was a POST request sent from this page
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form} 
    return render(request , 'base/room_form.html' , context)
 
@login_required(login_url='login')
def updateRoom(request ,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.user != room.host: # if user is trying to edit other people's room
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        form = RoomForm(request.POST , instance = room) # get data from the form
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request , 'base/room_form.html' , context)

@login_required(login_url='login')
def deleteRoom(request ,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host: # if user is trying to edit other people's room
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request , 'base/delete.html' , context)