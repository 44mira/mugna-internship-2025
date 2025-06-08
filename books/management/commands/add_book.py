from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Author
import requests

endpoint = "https://gutendex.com/books"


class Command(BaseCommand):
    help = f"Adds a book from Gutendex ({endpoint})"

    def add_arguments(self, parser):
        parser.add_argument("book_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        book_ids = (str(id) for id in options["book_ids"])
        r = requests.get(endpoint, params={"ids": ",".join(book_ids)})

        try:
            books = r.json()["results"]
        except:
            raise CommandError("There was an error in parsing the response.")

        for book in books:
            # if book exists, skip
            if Book.objects.filter(title=book["title"]):
                continue

            current_authors = []
            for author in book["authors"]:
                name = author["name"]
                last_name, first_name = (a.strip() for a in name.split(","))

                # if author exists, skip
                author = Author.objects.filter(
                    first_name=first_name, last_name=last_name
                )
                if author:
                    current_authors.append(author.first())
                    continue

                author = Author.objects.create(
                    first_name=first_name, last_name=last_name, email=""
                )
                current_authors.append(author)

            book_obj = Book.objects.create(title=book["title"])
            book_obj.authors.set(current_authors)

            self.stdout.write(self.style.SUCCESS(f"Added book '{book['title']}'."))
