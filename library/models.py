from django.db import models
from accounts.models import UserProfile
from books.models import Book


class LibraryBooks(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.user.username} is reading {self.book.title}"