from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from books.models import Book, Publisher, Author


class AuthorForm(forms.Form):
    author_name = forms.CharField(required=False)


class PublisherSearchForm(forms.Form):
    publisher_name = forms.CharField(required=False)


class PublisherPost(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class AuthorPost(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class BookPost(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class RegisterUser(forms.ModelForm):
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginUser(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. "
            "Note that both fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        self.user = None
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )

            if not self.user.is_active:
                raise forms.ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                )

        return self.cleaned_data
