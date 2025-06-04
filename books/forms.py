from django import forms

from books.models import Book, Publisher


class AuthorForm(forms.Form):
    author_name = forms.CharField(required=False)


class PublisherSearchForm(forms.Form):
    publisher_name = forms.CharField(required=False)


class PublisherPost(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookPost(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
