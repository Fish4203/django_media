from django.contrib.auth.models import User
from home.models import UserProfile
import requests
from .models import Class_info, CachSites
from django.shortcuts import redirect


def retreve(user, class_id, auth_token, args):
    response = {}

    ## get caching  object
    try:
        cach = CachSites.objects.filter(user=user).get(class_id=class_id)
    except:
        try:
            info =  Class_info.objects.filter(user=user).get(class_id=class_id)
        except:
            info = Class_info(user=user, class_id=class_id, notes='Welcome to your class page this is where you can access your clas info, modules, assignments, files, quizes and more. The buttons below arent linked to anything right now but you can change that by adding links using the eddit notes button above. If you cant see a module or assignment you cal always click the refresh button ')
            info.save()
        cach = CachSites(user=user, class_id=class_id, class_info=info)

    ## get class json
    if 'class' in args:
        try:
            if cach.class_json == '':
                raise ValueError

            response['class'] = cach.class_json
        except:
            try:
                url_class = f'https://jmss.instructure.com/api/v1/courses/{class_id}'
                headers = {"Authorization": f"Bearer {auth_token}"}

                response_class = requests.get(url_class, headers=headers)

                if response_class.status_code != 200:
                    raise ValueError

                response['class'] = response_class.json()


                cach.class_json = response_class.json()
                cach.name = response_class.json()['name']
                cach.course_code = response_class.json()['course_code']
                #cach.image_download_url = response_class.json()['image_download_url']

                cach.save()
            except:
                #print(response_class.status_code, response_class.json())
                response['error_class'] = 'could not get class data'

    ## get moules
    if 'modules' in args:
        try:
            if cach.modules_json == '':
                raise ValueError

            response['modules'] = cach.modules_json
        except:
            try:
                url_modules = f'https://jmss.instructure.com/api/v1/courses/{class_id}/modules'
                payload_modules = {'include': 'items', 'per_page': 1000}
                headers = {"Authorization": f"Bearer {auth_token}"}

                response_modules = requests.get(url_modules, headers=headers, params=payload_modules)

                if response_modules.status_code != 200:
                    raise ValueError

                response['modules'] = response_modules.json()

                cach.modules_json = response_modules.json()
                cach.save()
            except:
                response['error_modules'] = 'could not get moules'

    ## get assignments
    if 'assign' in args:
        try:
            if cach.assign_json == '':
                raise ValueError

            response['assign'] = cach.assign_json
        except:
            try:
                url_assign = f'https://jmss.instructure.com/api/v1/courses/{class_id}/assignments'
                payload_assign = {'include': 'submission', 'per_page': 1000, 'order_by': 'due_at'}
                headers = {"Authorization": f"Bearer {auth_token}"}

                response_assign = requests.get(url_assign, headers=headers, params=payload_assign)

                if response_assign.status_code != 200:
                    raise ValueError

                response['assign'] = response_assign.json()

                cach.assign_json = response_assign.json()
                cach.save()
            except:
                response['error_assign'] = 'could not get assignments'

    ## get frontpage
    if 'front_page' in args:
        try:
            if cach.frontpage_json == '':
                raise ValueError

            response['front_page'] = cach.frontpage_json
        except:
            try:
                url_front_page = f'https://jmss.instructure.com/api/v1/courses/{class_id}/front_page'
                headers = {"Authorization": f"Bearer {auth_token}"}

                response_front_page = requests.get(url_front_page, headers=headers)

                if response_front_page.status_code != 200:
                    raise ValueError

                response['front_page'] = response_front_page.json()

                cach.frontpage_json = response_front_page.json()
                cach.save()
            except:
                response['error_frontpage'] = 'could not get frontpage'


    ## get files json
    if 'files' in args:
        try:
            if cach.files_json == '':
                raise ValueError

            response['files'] = cach.files_json
        except:
            try:
                url_files = f'https://jmss.instructure.com/api/v1/courses/{class_id}/files'
                payload_files = {'include': 'items', 'per_page': 1000}
                headers = {"Authorization": f"Bearer {auth_token}"}

                response_files = requests.get(url_files, headers=headers, params=payload_files)

                if response_files.status_code != 200:
                    raise ValueError

                response['files'] = response_files.json()


                cach.files_json = response_files.json()

                cach.save()
            except:
                #print(response_class.status_code, response_class.json())
                response['error_files'] = 'could not get file data'


    ## Class info
    if 'class_info' in args:
        try:
            class_info = Class_info.objects.filter(user=user).filter(class_id=class_id)
            response['class_info'] = class_info
        except:
            response['error_info'] = 'could not get class info database lookup failed'

    #url_quiz = f'https://jmss.instructure.com/api/v1/courses/{class_id}/quizzes'
    #response_quiz = requests.get(url_quiz, headers=headers)

    return response



def add_classes(profile, auth_token, user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = 'https://jmss.instructure.com/api/v1/courses'
    payload_class = {'include': 'course_image', 'per_page': 1000}

    response = requests.get(url, headers=headers, params=payload_class)

    if response.status_code == 200:
        for clas in response.json():
            try:
                profile.canvas_classes.add(CachSites.objects.filter(user=user).get(class_id=clas['id']))
            except:
                try:
                    info =  Class_info.objects.filter(user=user).get(class_id=clas['id'])
                except:
                    info = Class_info(user=user, class_id=clas['id'], notes='Welcome to your class page this is where you can access your clas info, modules, assignments, files, quizes and more. The buttons below arent linked to anything right now but you can change that by adding links using the eddit notes button above. If you cant see a module or assignment you cal always click the refresh button ')
                    info.save()

                cach = CachSites(user=user, class_id=clas['id'], class_info=info, name=clas['name'], course_code=clas['course_code'], image_download_url=clas['image_download_url'])
                cach.save()

                profile.canvas_classes.add(cach)

        profile.save()
        return True
    else:
        return False


def get_auth_profile(user, session):
    # get user profile or rethuns index with error mesage
    try:
        profile = UserProfile.objects.get(user=user)
    except:
        context = 'failed to load user profile, Have you made a profile? are you signed in to the right user? if you have done these things contact me'
        return 'error', redirect('home:homePage',error=context)

    # get the auth token for the session or put the koken in the session
    try:
        auth_token = session['canvas_auth_token']
    except:
        try:
            session['canvas_auth_token'] = profile.canvas_token
            return 'error', redirect('compvas:index')
        except:
            context = 'failed to auth token, Have you made a profile? are you signed in to the right user? if you have done these things contact me'
            return 'error', redirect('home:homePage',error=context)

    return profile, auth_token



# import base64
# import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.fernet import Fernet
#
#
#
# def enc(data, password):
#     password_encode = password.encode()
#     data_encode = data.encode()
#     salt = os.urandom(16)
#
#     kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
#     )
#
#     f = Fernet(base64.urlsafe_b64encode(kdf.derive(password_encode)))
#
#     return f.encrypt(data_encode)
#
#
# def denc(data, password):
#     password_encode = password.encode()
#     salt = os.urandom(16)
#
#     kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
#     )
#
#     f = Fernet(base64.urlsafe_b64encode(kdf.derive(password_encode)))
#
#     return f.decrypt(data)
