from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from books.models import Author


class AuthTests(TestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "123123"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.admin_username = "test"
        self.admin_password = "123123"
        self.admin_email = "test@test.com"
        self.admin = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
            email=self.admin_email,
        )

    def test_login_user(self):
        response = self.client.post(
            reverse("login-user"),
            {"username": self.username, "password": self.password},
            follow=True,
        )

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.request["PATH_INFO"], "/index/")

        response = self.client.get(
            reverse("login-user"),
            follow=True,
        )
        self.assertEqual(response.request["PATH_INFO"], "/index/")

    def test_logout_superuser(self):
        response = self.client.get(reverse("logout-user"), follow=True)
        self.assertEqual(response.request["PATH_INFO"], "/login/")

        self.client.login(
            username=self.admin_username,
            password=self.admin_password,
            email=self.admin_email,
        )
        response = self.client.post(reverse("logout-user"), follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.request["PATH_INFO"], "/login/")
