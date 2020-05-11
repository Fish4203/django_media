from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('home/<str:error>', views.homePage, name='homePage'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('new_account', views.new_account, name='new_account'),
    path('signout', views.signout, name='signout')

]
