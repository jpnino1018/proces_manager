from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_processes, name='list_processes'),
    path('stop_process/<int:pid>/', views.stop_process, name='stop_process'),
]
