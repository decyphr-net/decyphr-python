"""
The Library model.

This model stores all of the information regarding a user their relationship
with a specific book. This will be the model that will be used to store the
user's reading list and their progress with the book
"""
from django.db import models
from accounts.models import UserProfile
from books.models import Book


class LibraryBook(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="books")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} is reading {self.book.title}"