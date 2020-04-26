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

def new_post(request):
    if request.POST['post_title'] == '' or request.POST['body_text'] == '':
        return render(request, 'polls/index', {
            'error_message': "The title or post body was blank",
        })

    try:
        post = Posts(title_text=request.POST['post_title'], body_text=request.POST['body_text'], user=request.user, date=timezone.now())
        post.save()

        return HttpResponseRedirect(reverse('message:index'))
    except:
        return render(request, 'polls/index', {
            'error_message': "Failed to create post",
        })
