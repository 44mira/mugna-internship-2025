from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return str(self.name)


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("books.Author", related_name="books")
    publisher = models.ForeignKey(
        "books.Publisher", on_delete=models.CASCADE, related_name="books"
    )
    classification = models.ForeignKey(
        "books.Classification",
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
    )

    def __str__(self):
        return str(self.title)


class Classification(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"({self.code}) {self.name}"
