from django.contrib import admin

from books.models import Author, Book, Publisher, Classification


class BookAdmin(admin.ModelAdmin):
    fields = ["title", "classification", "authors", "publisher"]


class PublisherAdmin(admin.ModelAdmin):
    fields = ["name", "website", "country", "city", "state_province"]
    search_fields = ["name", "city", "country", "website"]
    list_display = ["name", "city", "country", "website"]


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Classification)
