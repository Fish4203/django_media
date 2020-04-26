from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('delete<str:title>/', views.delete, name='delete'),
    path('new_post', views.new_post, name='new_post'),
]
