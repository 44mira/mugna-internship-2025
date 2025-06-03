from django.shortcuts import render
from books.models import Book, Author, Classification


# Create your views here.
def books(request):
    return render(request, "books.html", {"books": Book.objects.all()})


def book(request, pk):
    book = Book.objects.get(pk=pk)
    return render(
        request,
        "book.html",
        {
            "title": book.title,
            "authors": book.authors.all(),
            "publisher": book.publisher,
            "classification": book.classification,
        },
    )


def author(request, pk):
    author = Author.objects.get(pk=pk)
    return render(
        request,
        "author.html",
        {
            "author": str(author),
            "books": author.books.all(),
        },
    )


def classification(request, pk):
    classification = Classification.objects.get(pk=pk)

    return render(
        request,
        "classification.html",
        {
            "classification": classification,
            "books": classification.books.all(),
        },
    )
