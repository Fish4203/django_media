from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('AboutMe/', views.about, name='about'),
    path('algox', views.algox, name='algox'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout')

]
