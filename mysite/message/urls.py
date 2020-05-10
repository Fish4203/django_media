from django.urls import path
from . import views

app_name = 'message'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/<str:error>', views.index, name='index'),
    path('search', views.search, name='search'),
    path('delete/<str:title>/', views.delete, name='delete'),
    path('post_full/<str:title>/', views.post_full, name='post_full'),
    path('new_comment', views.new_comment, name='new_comment'),
    path('new_post', views.new_post, name='new_post'),
]
