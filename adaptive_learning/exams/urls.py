from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.exam_list,     name='exam_list'),
    path('<int:pk>/',                views.exam_detail,   name='exam_detail'),
    path('<int:pk>/start/',          views.start_exam,    name='start_exam'),
    path('<int:pk>/submit/',         views.submit_exam,   name='submit_exam'),
    path('create/',                  views.create_exam,   name='create_exam'),
    path('<int:pk>/add-question/',   views.add_question,  name='add_question'),
]