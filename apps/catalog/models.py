from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    name = models.CharField(max_length=20)
    biography = models.TextField(max_length=300, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"

    @property
    def total_books(self):
        return self.books.count()

class Publisher(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Genre(models.Model):
    class GenreType(models.TextChoices):
        EDUCATION = 'EDUCATION', 'Education'
        TECHNOLOGY = 'TECHNOLOGY', 'Technology'
        SELF_HELP = 'SELF_HELP', 'Self Help'
        FICTIONAL = 'FICTIONAL', 'Fictional'
        HORROR = 'HORROR', 'Horror'

    name = models.CharField(
        max_length=20, 
        choices=GenreType.choices,
        unique=True,
        )

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField()
    author = models.ManyToManyField(
        'Author', 
        related_name='books',
        blank=True,
    )
    publisher = models.ManyToManyField(
        'Publisher', 
        related_name='books',
        blank=True,
    )
    genres = models.ManyToManyField(
        'Genre',
        related_name='books',
        blank=True,
    )
    cover_image = models.ImageField(blank=True, upload_to='book_cover_images')
    isbn = models.CharField(max_length=13, unique=True, db_index=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        blank=True,
        )
    stock_quantity = models.PositiveIntegerField(default=0)
    publication_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1500),
            MaxValueValidator(2100),
        ]
    )
    language = models.CharField(default='English', max_length=10)
    description = models.TextField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['is_active', 'created_at']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(price__gte=0),
                name='book_price_non_negative',
            ),
        ]

    def __str__(self):
        return f"{self.title}"
