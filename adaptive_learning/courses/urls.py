from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.course_list,    name='course_list'),
    path('<int:pk>/',               views.course_detail,  name='course_detail'),
    path('<int:pk>/enroll/',        views.enroll_course,  name='enroll_course'),
    path('my-courses/',             views.my_courses,     name='my_courses'),
    path('create/',                 views.create_course,  name='create_course'),
    path('<int:pk>/add-module/',    views.add_module,     name='add_module'),
]