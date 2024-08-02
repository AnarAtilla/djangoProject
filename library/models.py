from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Staff', 'Staff'),
    ('Reader', 'Reader'),
]


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    profile = models.URLField(null=True, blank=True, verbose_name="Profile URL")
    deleted = models.BooleanField(
        default=False,
        verbose_name="Is Deleted",
        help_text="If False - author is active. If True - author is no longer available"
    )
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Author Rating"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name[0]}."


class Library(models.Model):
    name = models.CharField(max_length=100, verbose_name="Library Name")
    location = models.CharField(max_length=200, verbose_name="Location")
    site = models.URLField(null=True, blank=True, verbose_name="Website")

    def __str__(self):
        return self.name


class Member(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Reader', 'Reader'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name="Gender")
    birth_date = models.DateField(verbose_name="Birth Date")
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)], verbose_name="Age")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Role")
    active = models.BooleanField(default=True, verbose_name="Active")
    libraries = models.ManyToManyField('Library', related_name='members', verbose_name="Libraries")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    country = models.CharField(max_length=100, verbose_name="Country")

    def __str__(self):
        return self.name


class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Biography', 'Biography'),
    ]
    title = models.CharField(max_length=100, verbose_name="Book Title")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, verbose_name="Author")
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL, verbose_name="Publisher")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='books',
                                 verbose_name="Category")
    libraries = models.ManyToManyField(Library, related_name='books', blank=True, verbose_name="Libraries")
    publishing_date = models.DateField(verbose_name="Publishing Date")
    summary = models.TextField(null=True, blank=True, verbose_name="Summary")
    genre = models.CharField(max_length=50, null=True, choices=GENRE_CHOICES, verbose_name="Genre")
    page_count = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)],
                                     verbose_name="Page Count")

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.libraries.exists()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Posts(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Post Title")
    body = models.TextField(verbose_name="Post Body")
    author = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='posts', verbose_name="Author")
    moderated = models.BooleanField(default=False, verbose_name="Moderated")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='posts', verbose_name="Library")
    created_at = models.DateField(verbose_name="Created At")
    updated_at = models.DateField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title


class Borrow(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='borrows', verbose_name="Member")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='borrows', verbose_name="Book")
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='borrows', verbose_name="Library")
    borrow_date = models.DateField(verbose_name="Borrow Date")
    return_date = models.DateField(verbose_name="Return Date")
    returned = models.BooleanField(default=False, verbose_name="Returned")

    def is_overdue(self):
        if self.returned:
            return False
        return self.return_date < timezone.now().date()

    def mark_as_returned(self):
        self.returned = True
        self.save()

    @staticmethod
    def get_overdue_borrows():
        return Borrow.objects.filter(returned=False, return_date__lt=timezone.now().date())

    def __str__(self):
        return f"{self.member} borrowed '{self.book}' from '{self.library}'"

    class Meta:
        verbose_name = "Borrow Record"
        verbose_name_plural = "Borrow Records"


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews', verbose_name="Book")
    reviewer = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='reviews', verbose_name="Reviewer")
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    description = models.TextField(verbose_name="Review")

    def __str__(self):
        return f"Review on '{self.book}' by {self.reviewer}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class AuthorDetail(models.Model):
    author = models.OneToOneField('Author', on_delete=models.CASCADE, related_name='details')
    biography = models.TextField(verbose_name="Biography")
    birth_city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Birth City")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name="Gender")

    def __str__(self):
        return f"Details for {self.author}"

    class Meta:
        verbose_name = "Author Detail"
        verbose_name_plural = "Author Details"


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название события")
    description = models.TextField(verbose_name="Описание события")
    date = models.DateTimeField(verbose_name="Дата проведения события")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='events', verbose_name="Библиотека")
    books = models.ManyToManyField(Book, related_name='events', verbose_name="Книги")

    def __str__(self):
        return self.title


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', verbose_name="Событие")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='event_participations',
                               verbose_name="Участник")
    registration_date = models.DateField(default=timezone.now, verbose_name="Дата регистрации")

    def __str__(self):
        return f"{self.member} at {self.event}"
