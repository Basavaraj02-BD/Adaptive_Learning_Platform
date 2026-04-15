from django.urls import path
from . import views

urlpatterns = [
    path('',              views.my_results,    name='my_results'),
    path('<int:pk>/',     views.result_detail, name='result_detail'),
    path('notifications/',views.notifications, name='notifications'),
]