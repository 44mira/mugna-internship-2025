from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, UpdateView, View
from books.models import Book, Author, Classification, Publisher

from books.forms import (
    AuthorSearchForm,
    PublisherSearchForm,
    RegisterUser,
    LoginUser,
)


# Create your views here.
@login_required(login_url="/login/")
def books(request):
    return render(request, "books.html", {"books": Book.objects.all()})


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def author(request, pk):
    author = Author.objects.get(pk=pk)
    return render(
        request,
        "author.html",
        {
            "author": author,
            "books": author.books.all(),
        },
    )


@login_required(login_url="/login/")
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


class AuthorSearch(LoginRequiredMixin, View):
    login_url = "/login/"
    form_class = AuthorSearchForm
    template_name = "search_author.html"

    def get(self, request, *args, **kwargs):
        if "author_name" in request.GET:
            form = self.form_class(request.GET)
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
                    self.template_name,
                    {"form": form, "authors": authors},
                )

        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class PublisherSearch(LoginRequiredMixin, View):
    login_url = "/login/"
    form_class = PublisherSearchForm
    template_name = "search_publisher.html"

    def get(self, request, *args, **kwargs):
        if "publisher_name" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                publisher_name = form.cleaned_data["publisher_name"]
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "publishers": Publisher.objects.filter(
                            name__icontains=publisher_name
                        ),
                    },
                )
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class BookPost(UserPassesTestMixin, CreateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Book
    fields = "__all__"

    success_url = "/books/"
    template_name = "post_entity.html"
    extra_context = {"entity": "book"}


class PublisherPost(UserPassesTestMixin, CreateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Publisher
    fields = "__all__"

    success_url = "/search-publisher/"
    template_name = "post_entity.html"
    extra_context = {"entity": "publisher"}


class AuthorPost(UserPassesTestMixin, CreateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Author
    fields = "__all__"

    success_url = "/search-author/"
    template_name = "post_entity.html"
    extra_context = {"entity": "author"}


class BookDelete(UserPassesTestMixin, DeleteView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Book

    success_url = "/books/"
    template_name = "delete_entity.html"
    extra_context = {"entity": "book"}


class PublisherDelete(UserPassesTestMixin, DeleteView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Publisher

    success_url = "/search-publisher/"
    template_name = "delete_entity.html"
    extra_context = {"entity": "publisher"}


class AuthorDelete(UserPassesTestMixin, DeleteView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Author

    success_url = "/search-author/"
    template_name = "delete_entity.html"
    extra_context = {"entity": "author"}


class BookPut(UserPassesTestMixin, UpdateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Book
    fields = "__all__"

    success_url = "/books/"
    template_name = "put_entity.html"

    def get_context_data(self, **kwargs):
        return {"entity": "book", "obj": self.get_object()}


class PublisherPut(UserPassesTestMixin, UpdateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Publisher
    fields = "__all__"

    success_url = "/search-publisher/"
    template_name = "put_entity.html"

    def get_context_data(self, **kwargs):
        return {"entity": "publisher", "obj": self.get_object()}


class AuthorPut(UserPassesTestMixin, UpdateView):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.is_superuser

    model = Author
    fields = "__all__"

    success_url = "/search-author/"
    template_name = "put_entity.html"

    def get_context_data(self, **kwargs):
        return {"entity": "author", "obj": self.get_object()}


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


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/index/")

    form = LoginUser()

    if request.method == "POST":
        form = LoginUser(request.POST)
        if form.is_valid():
            user = form.user

            # valid login is already checked within LoginUser
            login(request, user)
            return HttpResponseRedirect("/index/")

    context = {"form": form}
    return render(request, "login_user.html", context)


@login_required(login_url="/login/")
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect("/login/")

    return render(request, "logout_user.html")
