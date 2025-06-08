from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from books.models import Author
from books.forms import AuthorSearchForm


class AuthorTests(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )

        self.username = "test"
        self.password = "123123"
        self.admin = User.objects.create_superuser(
            username=self.username, password=self.password, email="test@test.com"
        )

    def test_post_author(self):
        self.client.login(
            username=self.username, password=self.password, email="test@test.com"
        )

        expected_kwargs = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
        }

        response = self.client.post(
            reverse("post-author"), expected_kwargs, follow=True
        )

        self.assertIsNotNone(Author.objects.filter(**expected_kwargs))
        self.assertEqual(response.request["PATH_INFO"], "/search-author/")

    def test_delete_author(self):
        self.client.login(
            username=self.username,
            password=self.password,
            email="test@test.com",
        )
        response = self.client.post(
            reverse("delete-author", kwargs={"pk": 1}), follow=True
        )

        self.assertFalse(Author.objects.exists())
        self.assertEqual(response.request["PATH_INFO"], "/search-author/")

    def test_put_author(self):
        self.client.login(
            username=self.username, password=self.password, email="test@test.com"
        )

        expected_kwargs = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "updated@example.com",
        }

        response = self.client.post(
            reverse("put-author", kwargs={"pk": 1}),
            expected_kwargs,
            follow=True,
        )

        self.assertEqual(model_to_dict(Author.objects.get(pk=1)), expected_kwargs)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(response.request["PATH_INFO"], "/search-author/")
