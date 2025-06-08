from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from books.models import Publisher, Author


class SearchTests(TestCase):
    def setUp(self):
        # Create two publishers
        self.publisher1 = Publisher.objects.create(
            name="Alpha Books",
            address="100 Alpha St",
            city="Alphatown",
            state_province="AP",
            country="Wonderland",
            website="https://alpha.example.com",
        )

        self.publisher2 = Publisher.objects.create(
            name="Beta Publishing",
            address="200 Beta Ave",
            city="Betaville",
            state_province="BP",
            country="Utopia",
            website="https://beta.example.com",
        )

        # Create two authors
        self.author1 = Author.objects.create(
            first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )

        self.author2 = Author.objects.create(
            first_name="John", last_name="Smith", email="john.smith@example.com"
        )

        self.username = "test"
        self.password = "123123"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_search_author(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("search-author", query=[("name", "John")]))

        self.assertListEqual(
            list(response.context["authors"]),
            list(Author.objects.filter(first_name="John")),
        )

    def test_search_publisher(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse("search-publisher", query=[("name", "Alpha Books")])
        )

        self.assertListEqual(
            list(response.context["publishers"]),
            list(Publisher.objects.filter(name="Alpha Books")),
        )
