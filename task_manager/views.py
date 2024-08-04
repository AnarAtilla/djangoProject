from django.shortcuts import render

from .models import Task, Category


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'task_manager/category_list.html', {'categories': categories})