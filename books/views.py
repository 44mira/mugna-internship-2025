from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from books.models import Book, Author, Classification, Publisher

from books.forms import (
    AuthorForm,
    BookPost,
    PublisherPost,
    PublisherSearchForm,
    RegisterUser,
)


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


def search_author(request):
    if "author_name" in request.GET:
        form = AuthorForm(request.GET)
        if form.is_valid():
            author_name = form.cleaned_data["author_name"]

            # concatenate first_name and last_name to filter both names at the
            # same time
            named_authors = Author.objects.annotate(
                full_name=Concat("first_name", Value(" "), "last_name")
            )
            authors = named_authors.filter(full_name__icontains=author_name)

            return render(
                request,
                "search_author.html",
                {"form": form, "authors": authors},
            )
    form = AuthorForm()
    return render(request, "search_author.html", {"form": form})


def search_publisher(request):
    if "publisher_name" in request.GET:
        form = PublisherSearchForm(request.GET)
        if form.is_valid():
            publisher_name = form.cleaned_data["publisher_name"]
            return render(
                request,
                "search_publisher.html",
                {
                    "form": form,
                    "publishers": Publisher.objects.filter(
                        name__icontains=publisher_name
                    ),
                },
            )
    form = PublisherSearchForm()
    return render(request, "search_publisher.html", {"form": form})


def post_book(request):
    form = BookPost()

    if request.method == "POST":
        form = BookPost(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/books/")

    return render(request, "post_entity.html", {"entity": "book", "form": form})


def post_publisher(request):
    form = PublisherPost()

    if request.method == "POST":
        form = PublisherPost(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/search-publisher/")

    return render(request, "post_entity.html", {"entity": "publisher", "form": form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return HttpResponseRedirect("/books/")

    context = {"entity": "book", "obj": book}
    return render(request, "delete_entity.html", context)


def delete_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)

    if request.method == "POST":
        publisher.delete()
        return HttpResponseRedirect("/search-publisher/")

    context = {"entity": "publisher", "obj": publisher}
    return render(request, "delete_entity.html", context)


def put_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookPost(instance=book)

    if request.method == "POST":
        form = BookPost(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/book/{pk}")

    context = {"entity": "book", "obj": book, "form": form}
    return render(request, "put_entity.html", context)


def put_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    form = PublisherPost(instance=publisher)

    if request.method == "POST":
        form = PublisherPost(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/search-publisher/")

    context = {"entity": "publisher", "obj": publisher, "form": form}
    return render(request, "put_entity.html", context)


def register_user(request):
    form = RegisterUser()

    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/index/")

    context = {"form": form}
    return render(request, "register_user.html", context)
