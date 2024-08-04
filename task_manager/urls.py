from django.urls import path

from . import views

app_name = 'task_manager'

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('categories/', views.category_list, name='category_list'),
]