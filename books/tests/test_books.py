from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from books.models import Book, Publisher, Classification, Author


class BookGetTest(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="Fictional Press",
            address="123 Fictional St",
            city="Storyville",
            state_province="SP",
            country="Neverland",
            website="https://fictionalpress.example.com",
        )

        # Create a classification
        self.classification = Classification.objects.create(
            code="ABC", name="Fiction", description="Fictional books"
        )

        # Create authors
        self.author1 = Author.objects.create(
            first_name="Alice", last_name="Smith", email="alice@example.com"
        )

        self.author2 = Author.objects.create(
            first_name="Bob", last_name="Jones", email="bob@example.com"
        )

        # Create books
        self.book1 = Book.objects.create(
            title="The First Tale",
            publisher=self.publisher,
            classification=self.classification,
        )
        self.book1.authors.set([self.author1])

        self.book2 = Book.objects.create(
            title="The Second Tale",
            publisher=self.publisher,
            classification=self.classification,
        )
        self.book2.authors.set([self.author1, self.author2])

        self.username = "test"
        self.password = "123123"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_book_list(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("books"))

        self.assertListEqual(list(response.context["books"]), list(Book.objects.all()))

    def test_book_detail(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("book", kwargs={"pk": 1}))

        expected = Book.objects.get(pk=1)

        self.assertEqual(response.context["title"], expected.title)
        self.assertEqual(response.context["publisher"], expected.publisher)
        self.assertEqual(response.context["classification"], expected.classification)
        self.assertListEqual(
            list(response.context["authors"]), list(expected.authors.all())
        )
