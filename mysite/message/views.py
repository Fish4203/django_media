from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from message.models import Posts



def index(request):
    context = {"additional_context": {'a': 'posts', 'b': 'index'}, 'posts': Posts.objects.all()}
    return render(request, 'message/index.html', context)

def search(request):
    if request.POST['search_text'] != '':
        posts = Posts.objects.filter(title_text__contains=request.POST['search_text'])
    else:
        posts = Posts.objects.all()
    context = {"additional_context": {'a': 'posts', 'b': 'index'}, 'posts': posts}
    return render(request, 'message/index.html', context)

def delete(request, title):
    try:
        post = Posts.objects.get(title_text=title)
        if post.user == request.user:
            post.delete()
            return HttpResponseRedirect(reverse('message:index'))
        else:
            return render(request, 'message/index', {
                'error_message': "Failed to authenticate",
            })
    except:
        return render(request, 'message/index', {
            'error_message': "Failed to find post",
        })

def new_post(request):
    if request.POST['post_title'] == '' or request.POST['body_text'] == '':
        return render(request, 'message/index', {
            'error_message': "The title or post body was blank",
        })

    try:
        post = Posts(title_text=request.POST['post_title'], body_text=request.POST['body_text'], img_link=request.POST['img_link'], user=request.user, date=timezone.now())
        post.save()

        return HttpResponseRedirect(reverse('message:index'))
    except:
        return render(request, 'message/index', {
            'error_message': "Failed to create post",
        })
