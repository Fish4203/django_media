from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#from message.models import Posts
# Create your views here.


def homePage(request):
    context = {"additional_context": {'a': 'home'}}
    return render(request, 'home/homepage.html', context)

def about(request):
    context = {"additional_context": {'a': 'about'}}
    return render(request, 'home/about.html', context)

def algox(request):
    context = {"additional_context": {'a': 'algox'}}
    return render(request, 'home/algox.html', context)

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        print('it work')
        return HttpResponseRedirect(reverse('home:homePage'))
    else:
        return render(request, 'home/homepage.html', {
            'error_message': "invalid username or password",
        })

def new_account(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()

        return HttpResponseRedirect(reverse('home:homePage'))
    except:
        return render(request, 'home/homepage.html', {
            'error_message': "could not create account",
        })



def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:homePage'))
