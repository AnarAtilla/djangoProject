from django.shortcuts import get_object_or_404, render

from library.models import Book


def home(request):
    return render(request, 'library/home.html')


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {
        'category': category,
    }
    return render(request, 'task_manager/category_list.html', context)

def djangohome(request):
    return render(request, 'djangohome.html')