from django.test import TestCase
from django.db import IntegrityError
from .models import *

# Negative book prices are rejected
# Negative stock is rejected
# Duplicate ISBNs are rejected
# Invalid publication years are rejected
# Books can have multiple genres
# Deleting an author with books is prevented
# Inactive books remain stored

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='James',
            last_name='Clear',
            biography='Good Author',
        )

    def test_author_names_cannot_be_duplicated(self):
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                first_name='James',
                last_name='Clear',
                biography='Good Author',
            )

    def test_author_total_name_count_is_one (self):
        self.assertEqual(Author.objects.count(), 1)

class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name='EDUCATION',
        )

    def test_genres_cannot_be_duplicated(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(
                name='EDUCATION',
            )
        
class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            # title
            # isbn
            # author
            # genres
            # price
            # stock_quantity
            # publication_year
            # description
            # is_active

        )