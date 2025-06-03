from django.contrib import admin

from books.models import Author, Book, Publisher, Classification

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Classification)
