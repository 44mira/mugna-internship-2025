from django.urls import path
from books.views import books, book, author

urlpatterns = [
    path("books/", books, name="books"),
    path("book/<int:pk>/", book, name="book"),
    path("author/<int:pk>/", author, name="author"),
]
