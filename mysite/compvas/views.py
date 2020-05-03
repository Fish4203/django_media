from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests

import environ
env = environ.Env(
    # set casting, default value
)
environ.Env.read_env()

auth_token = env('AUTH_TOKEN')

def index(request):
    global auth_token
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = 'https://jmss.instructure.com/api/v1/courses'
    payload_class = {'include': 'course_image'}

    response = requests.get(url, headers=headers, params=payload_class)
    context = {"additional_context": {'a': 'compvas', 'b': 'index'}, 'classes': response.json()}
    return render(request, 'compvas/index.html', context)


def classes(request, class_id):
    global auth_token

    url_class = f'https://jmss.instructure.com/api/v1/courses/{class_id}'
    url_assign = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments'
    url_modules = f'https://jmss.instructure.com/api/v1/courses/{class_id}/modules'
    url_quiz = f'https://jmss.instructure.com/api/v1/courses/{class_id}/quizzes'

    payload_modules = {'include': 'items'}
    payload_assign = {'include': 'items'}

    headers = {"Authorization": f"Bearer {auth_token}"}

    response_class = requests.get(url_class, headers=headers)
    response_assign = requests.get(url_assign, headers=headers, params=payload_assign)
    response_modules = requests.get(url_modules, headers=headers, params=payload_modules)
    response_quiz = requests.get(url_quiz, headers=headers)

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'class': response_class.json(), 'modules': response_modules.json(), 'assign': response_assign.json(), 'quizes': response_quiz.json()}
    return render(request, 'compvas/class.html', context)


def module_item(request, class_id, module_name):
    global auth_token

    url_class = f'https://jmss.instructure.com/api/v1/courses/{class_id}'
    url_assign = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments'
    url_modules = f'https://jmss.instructure.com/api/v1/courses/{class_id}/modules'
    url_module_item = f'https://jmss.instructure.com/api/v1/courses/{class_id}/pages/{module_name}'

    payload_module_item = {'include': 'items'}
    payload_modules = {'include': 'items'}
    payload_assign = {'include': 'items'}

    headers = {"Authorization": f"Bearer {auth_token}"}

    response_class = requests.get(url_class, headers=headers)
    response_assign = requests.get(url_assign, headers=headers, params=payload_assign)
    response_modules = requests.get(url_modules, headers=headers, params=payload_modules)
    response_module_item = requests.get(url_module_item, headers=headers, params=payload_module_item)

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'class': response_class.json(), 'module_item': response_module_item.json(), 'modules': response_modules.json(), 'assign': response_assign.json()}
    return render(request, 'compvas/module_item.html', context)


def assignment_item(request, class_id, assignment_name):
    global auth_token

    url_class = f'https://jmss.instructure.com/api/v1/courses/{class_id}'
    url_assign = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments'
    url_modules = f'https://jmss.instructure.com/api/v1/courses/{class_id}/modules'
    url_assignment_item = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments/{assignment_name}'

    payload_assignment_item = {'include': 'submission'}
    payload_modules = {'include': 'items'}
    payload_assign = {'include': 'items'}

    headers = {"Authorization": f"Bearer {auth_token}"}

    response_class = requests.get(url_class, headers=headers)
    response_assign = requests.get(url_assign, headers=headers, params=payload_assign)
    response_modules = requests.get(url_modules, headers=headers, params=payload_modules)
    response_assignment_item = requests.get(url_assignment_item, headers=headers, params=payload_assignment_item)

    context = {"additional_context": {'a': 'compvas', 'b': class_id}, 'class': response_class.json(), 'assignment_item': response_assignment_item.json(), 'modules': response_modules.json(), 'assign': response_assign.json()}
    return render(request, 'compvas/assignment_item.html', context)


def new_submission(request, class_id, assignment_name):
    global auth_token

    url_submission = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments/{assignment_name}/submissions'

    if 'http' in request.POST['sub_input']:
        payload_assignment_item = {'submission[submission_type]': 'online_url', 'submission[url]': request.POST['sub_input'], 'comment[text_comment]': request.POST['comment'] }
    else:
        payload_submission = {'submission[submission_type]': 'online_text_entry', 'submission[body]': request.POST['sub_input']}

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response_assignment_item = requests.post(url_submission, headers=headers, params=payload_submission)

        if response_assignment_item.status_code == 201:
            return HttpResponseRedirect(reverse('compvas:index'))
        else:
            return render(request, 'compvas/index.html', {
                'error_message': f"Failed to make submission error {response_assignment_item.status_code}",
            })
    except:
        return render(request, 'compvas/index.html', {
            'error_message': f"Failed to make submission error {response_assignment_item.status_code}",
        })



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
