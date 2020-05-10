from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('index/<str:error>', views.Index.as_view(), name='index'),
    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('<int:pk>/results/', views.Results.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/delete/', views.delete, name='delete'),
    path('new_question/', views.new_question, name='new_question'),
]
