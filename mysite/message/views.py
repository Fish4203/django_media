from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from message.models import Posts, Comments



def index(request, error=''):
    context = {"additional_context": {'a': 'posts', 'b': 'index'}, 'error_message': error, 'posts': Posts.objects.all()}
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
            return redirect('message:index')
        else:
            return redirect('message:index', error="Failed to authentecate")
    except:
        return redirect('message:index', error="Failed to find post")


def post_full(request, title):
    post = Posts.objects.get(title_text=title)

    context = {'post': post}
    return render(request, 'message/post.html', context)

def new_comment(request):
    user=request.user
    date=timezone.now()
    comment_text = request.POST['comment_text']

    try:
        comment = Comments(comment_text=comment_text, user=user, date=date)
        comment.save()
    except:
        return redirect('message:index', error="Failed to make comment")

    try:
        if request.POST['submission_type'] == 'post':
            post = Posts.objects.get(id=int(request.POST['post_top']))
            post.comment_link.add(comment)
            post.save()
            return redirect('message:post_full', title=post.title_text)
        else:
            post = Comments.objects.get(id=int(request.POST['post_top']))
            print('22222222222')
            post.comment_link.add(comment)
            post.save()
            print('333333')
            return redirect('message:post_full', title=request.POST['submission_type'])

    except:
        return redirect('message:index', error="Failed to add to post or comment")


def new_post(request):
    if request.POST['post_title'] == '' or request.POST['body_text'] == '':
        return redirect('message:index', error="The title or body was blank")

    try:
        post = Posts(title_text=request.POST['post_title'], body_text=request.POST['body_text'], img_link=request.POST['img_link'], user=request.user, date=timezone.now())
        post.save()

        return redirect('message:index')
    except:
        return redirect('message:index', error="Failed to create post")
