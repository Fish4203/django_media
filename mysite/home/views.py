from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile

#from message.models import Posts




# Create your views here.


def homePage(request, error=''):
    print(error, 'rrrrrrrrrr')
    context = {"additional_context": {'a': 'home'}, 'error_message': error}
    return render(request, 'home/homepage.html', context)

def profile(request):
    # get user profile or rethuns index with error mesage
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = UserProfile(user=request.user)
        profile.save()

    context = {"additional_context": {'a': 'profile'}, 'profile': profile}
    return render(request, 'home/profile.html', context)

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        #print(user)
        if user is not None:
            login(request, user)
            #print('it work')
            return redirect('home:homePage')
        else:
            context = {'error_message': 'could not authentecate account'}
            return render(request, 'home/signin.html', context)

    elif request.method == 'GET':
        return render(request, 'home/signin.html')

def update_profile(request):
    profile_data = get_object_or_404(UserProfile, user=request.user)

    try:
        profile_data.user.email = request.POST['email']
        profile_data.calender_link = request.POST['calender_link']
        profile_data.profile_picture = request.POST['profile_picture']
        profile_data.canvas_token = request.POST['canvas_token']

        #print(profile_data)

        profile_data.save()

        return redirect('home:profile')
    except:
        context = 'an error ocured updating the profile'
        return redirect('home:homePage', error=context)



def new_account(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()

            context = 'sucsessfuly created new account'
            return redirect('home:homePage', error=context)
        except:
            context = {'error_message': 'could not created new account'}
            return render(request, 'home/new_account.html', context)

    elif request.method == 'GET':
        return render(request, 'home/new_account.html')


def signout(request):
    logout(request)
    return redirect('home:homePage')
