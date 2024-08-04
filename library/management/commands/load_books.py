import csv

from django.core.management.base import BaseCommand

from library.models import Book, Author, Library, Category, Publisher


class Command(BaseCommand):
    help = 'Load books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load books from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_title = row['title']
                author_name = row['author'].split()  # Разделение имени и фамилии
                first_name = author_name[0]
                last_name = author_name[1] if len(author_name) > 1 else ''
                library_names = row['libraries'].split(',')
                publishing_date = row['publishing_date']
                category_name = row['category']
                publisher_name = row['publisher']
                genre = row['genre']
                page_count = int(row['page_count']) if row['page_count'] else None
                birth_date = row['birth_date'] if row['birth_date'] and row['birth_date'] != '***' else None

                # Create or get the author
                author, _ = Author.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    defaults={'birth_date': birth_date}
                )

                # Create or get the category
                category, _ = Category.objects.get_or_create(name=category_name)

                # Create or get the publisher
                publisher, _ = Publisher.objects.get_or_create(name=publisher_name)

                # Create or get the book
                book, created = Book.objects.get_or_create(
                    title=book_title,
                    author=author,
                    publisher=publisher,
                    category=category,
                    publishing_date=publishing_date,
                    genre=genre,
                    page_count=page_count
                )

                # Add libraries to the book
                for library_name in library_names:
                    library, _ = Library.objects.get_or_create(name=library_name)
                    book.libraries.add(library)

                self.stdout.write(self.style.SUCCESS(f'Successfully loaded book "{book_title}"'))