from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.models import UserProfile
import requests
from .models import Class_info, CachSites
from .utils import retreve, add_classes, get_auth_profile
from django.contrib.auth.decorators import login_required




def index(request, error=''):
    #
    # get user profile or rethuns index with error mesage
    profile, auth_token = get_auth_profile(request.user, request.session)
    if profile == 'error':
        return auth_token

    try:
        calender = profile.calender_link
    except:
        calender = None
        error = 'could not get clender'

    if profile.canvas_classes.all().count() == 0:
        class_acess = add_classes(profile=profile, user=request.user, auth_token=auth_token)

        if not class_acess:
            error = 'Your canvas token didnt work if you havent set a token then go to your profile and set the tokin'

    class_info = Class_info.objects.filter(user=request.user)

    assignments = {}
    for i in class_info:
        response = retreve(user=request.user, class_id=i.class_id, auth_token=auth_token, args=['assign'])

        assignments[str(i.class_id)] = response

    context = {"additional_context": {'a': 'compvas', 'b': 'index'}, 'assignments': assignments, 'profile': profile, 'error_message': error, 'class_info': class_info, 'calender': calender, 'classes': profile.canvas_classes.all()}
    return render(request, 'compvas/index.html', context)



def index_refresh(request):
    for cach in UserProfile.objects.get(user=request.user).canvas_classes.all():
        cach.delete()
    return redirect('compvas:index')




def classes(request, class_id):

    profile, auth_token = get_auth_profile(request.user, request.session)
    if profile == 'error':
        return auth_token

    # geting the other context data
    response = retreve(user=request.user, class_id=class_id, auth_token=auth_token, args=['class', 'assign', 'modules', 'class_info', 'front_page', 'files'])

    # formating the context
    context = {"additional_context": {'a': 'compvas', 'b': str(class_id)}, 'profile': profile} #, 'class': response_class.json(), 'modules': response_modules.json(), 'assign': response_assign.json()} #, 'quizes': response_quiz.json()
    context.update(response)
    return render(request, 'compvas/class.html', context)


def classes_refresh(request, class_id):
    cach = CachSites.objects.filter(user=request.user).get(class_id=class_id)
    cach.class_json = ''
    cach.modules_json = ''
    cach.assign_json = ''
    cach.frontpage_json = ''
    cach.save()

    return redirect('compvas:classes', class_id=class_id)




def module_item(request, class_id, module_name):
    # get user profile or rethuns index with error mesage
    profile, auth_token = get_auth_profile(request.user, request.session)
    if profile == 'error':
        return auth_token

    url_module_item = f'https://jmss.instructure.com/api/v1/courses/{class_id}/pages/{module_name}'

    payload_module_item = {'include': 'items', 'per_page': 1000}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_module_item = requests.get(url_module_item, headers=headers, params=payload_module_item)

    response = retreve(user=request.user, class_id=class_id, auth_token=auth_token, args=['class', 'assign', 'modules'])

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'profile': profile, 'module_item': response_module_item.json()}
    context.update(response)
    return render(request, 'compvas/module_item.html', context)



def assignment_item(request, class_id, assignment_name):
    # get user profile or rethuns index with error mesage
    profile, auth_token = get_auth_profile(request.user, request.session)
    if profile == 'error':
        return auth_token

    url_assignment_item = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments/{assignment_name}'
    payload_assignment_item = {'include': 'submission', 'per_page': 1000}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_assignment_item = requests.get(url_assignment_item, headers=headers, params=payload_assignment_item)

    response = retreve(user=request.user, class_id=class_id, auth_token=auth_token, args=['class', 'assign', 'modules'])

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'profile': profile, 'assignment_item': response_assignment_item.json()}
    context.update(response)
    return render(request, 'compvas/assignment_item.html', context)



def new_submission(request, class_id, assignment_name):
    #global auth_token

    profile, auth_token = get_auth_profile(request.user, request.session)
    if profile == 'error':
        return auth_token

    url_submission = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments/{assignment_name}/submissions'

    if 'http' in request.POST['sub_input']:
        payload_assignment_item = {'submission[submission_type]': 'online_url', 'submission[url]': request.POST['sub_input'], 'comment[text_comment]': request.POST['comment'] }
    else:
        payload_submission = {'submission[submission_type]': 'online_text_entry', 'submission[body]': request.POST['sub_input']}

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response_assignment_item = requests.post(url_submission, headers=headers, params=payload_submission)

        if response_assignment_item.status_code == 201:
            return redirect('compvas:assignment_item', class_id=class_id, assignment_name=assignment_name)
        else:
            return redirect('compvas:index', error=f"Failed to make submission error {response_assignment_item.status_code}")

    except:
        return redirect('compvas:index', error=f"Failed to make submission error {response_assignment_item.status_code}")



def new_notes(request, class_id):
    try:
        user = request.user
        notes = request.POST['notes']
        compass_link = request.POST['compass_link']
        google_sites = request.POST['google_sites']
        other_resource = request.POST['other_resource']
    except:
        return redirect('compvas:index', error="Failed to gae data")

    try:
        try:
            info = Class_info.objects.filter(user=request.user).get(class_id=class_id)

            info.notes = notes
            info.compass_link = compass_link
            info.google_sites = google_sites
            info.other_resource = other_resource


            info.save()

            return redirect('compvas:classes', class_id=class_id)
        except:
            #print(user, notes, class_id)
            info = Class_info(user=user, class_id=class_id, notes=notes, compass_link=compass_link, google_sites=google_sites, other_resource=other_resource)
            #print(info)
            info.save()

            return redirect('compvas:classes', class_id=class_id)
    except:
        return redirect('compvas:index', error="Failed to make notes")



'''
def quiz_item(request, class_id, quiz_name):
    url_class = f'https://jmss.instructure.com/api/v1/courses/{class_id}'
    url_assign = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments'
    url_modules = f'https://jmss.instructure.com/api/v1/courses/{class_id}/modules'
    url_quiz_sub = f'https://jmss.instructure.com/api/v1/courses/{class_id}/quizes/{quiz_name}/submissions'

    headers = {"Authorization": "Bearer 12164~YRlGQIB0HtzQ6p6aApGTl57XMyEJSCr8vCNWTsw8uViiRXLQEU3v5MnpmO4XJjZT"}

    response_quiz = requests.get(url_quiz_sub, headers=headers)

    payload_module_item = {'attempt': response_quiz.json()['attempt'], 'validation_token': response_quiz.json()['validation_token'] }
    payload_modules = {'include': 'items'}
    payload_assign = {'include': 'items'}

    url_quiz_item = f'https://jmss.instructure.com/api/v1/quiz_submissions/{response_quiz.json()['submission_id']}/questions'

    response_class = requests.get(url_class, headers=headers)
    response_assign = requests.get(url_assign, headers=headers, params=payload_assign)
    response_modules = requests.get(url_modules, headers=headers, params=payload_modules)
    response_quiz_item = requests.get(url_quiz_item, headers=headers, params=payload_quiz_item)

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'class': response_class.json(), 'quiz_item': response_quiz_item.json(), 'modules': response_modules.json(), 'assign': response_assign.json()}
    return render(request, 'compvas/quiz_item.html', context)
'''
