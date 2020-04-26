from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_post', views.new_post, name='new_post'),
]
