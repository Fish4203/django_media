from django.urls import path
from . import views

app_name = 'compvas'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/<str:error>', views.index, name='index'),
    path('index_refresh', views.index_refresh, name='index_refresh'),
    path('<str:class_id>/classes', views.classes, name='classes'),
    path('<str:class_id>/classes_refresh', views.classes_refresh, name='classes_refresh'),
    path('<str:class_id>/module_item/<str:module_name>', views.module_item, name='module_item'),
    path('<str:class_id>/assignment_item/<str:assignment_name>', views.assignment_item, name='assignment_item'),
    path('<str:class_id>/new_submission/<str:assignment_name>', views.new_submission, name='new_submission'),
    path('<str:class_id>/new_notes', views.new_notes, name='new_notes'),
    #path('<str:class_id>/quiz_item/<str:quiz_name>', views.quiz_item, name='quiz_item'),
]
