from django.shortcuts import get_object_or_404, render

from library.models import Book


def home(request):
    return render(request, 'library/home.html')


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'library/book_detail.html', context)
