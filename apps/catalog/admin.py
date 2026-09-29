from django.contrib import admin
from .models import Author, Publisher, Genre, Book


class BookInline(admin.TabularInline):
    model = Book.author.through
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['id', 'name', 'total_books']
    list_display_links = ['name',]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Publisher)
admin.site.register(Genre)