from django.urls import path
from books.views import (
    books,
    book,
    author,
    delete_book,
    delete_publisher,
    search_author,
    search_publisher,
    post_book,
    post_publisher,
    put_book,
    put_publisher,
    classification,
    register_user,
)

urlpatterns = [
    path("books/", books, name="books"),
    path("book/<int:pk>/", book, name="book"),
    path("author/<int:pk>/", author, name="author"),
    path("search-author/", search_author, name="search-author"),
    path("search-publisher/", search_publisher, name="search-publisher"),
    path("classification/<int:pk>/", classification, name="classification"),
    path("post/book/", post_book, name="post-book"),
    path("post/publisher/", post_publisher, name="post-publisher"),
    path("delete/book/<int:pk>/", delete_book, name="delete-book"),
    path("delete/publisher/<int:pk>/", delete_publisher, name="delete-book"),
    path("put/book/<int:pk>/", put_book, name="put-book"),
    path("put/publisher/<int:pk>/", put_publisher, name="put-publisher"),
    path("register/", register_user, name="register-user"),
]
