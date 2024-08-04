from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Author, AuthorDetail, Book

def custom_404(request, _):
    return render(request, '404.html', status=404)

@login_required
def home(request):
    books = Book.objects.all()[:20]  # Ограничение до 20 книг
    authors = Author.objects.all()
    genres = Book.GENRE_CHOICES

    author_id = request.GET.get('author')
    genre = request.GET.get('genre')
    year = request.GET.get('year')
    date = request.GET.get('date')

    if author_id:
        books = books.filter(author_id=author_id)
    if genre:
        books = books.filter(genre=genre)
    if year:
        books = books.filter(publishing_date__year=year)
    if date:
        books = books.filter(publishing_date=date)

    context = {
        'books': books,
        'authors': authors,
        'genres': genres,
    }
    return render(request, 'library/home.html', context)

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    try:
        author_details = AuthorDetail.objects.get(author=author)
    except AuthorDetail.DoesNotExist:
        return render(request, 'author_updating.html', {'author': author})

    return render(request, 'author_detail.html', {'author': author, 'author_details': author_details})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'library/book_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})