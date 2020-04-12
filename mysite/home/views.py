from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse, HttpResponseRedirect
#from django.urls import reverse
#from django.views import generic
#from django.utils import timezone
# Create your views here.


def homePage(request):
    context = {"additional_context": {'a': 'home'}}
    return render(request, 'home/homepage.html', context)

def about(request):
    context = {"additional_context": {'a': 'about'}}
    return render(request, 'home/about.html', context)
