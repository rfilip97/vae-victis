from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """Stores data fetched from Google Books API or manually entered data."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class UserBook(models.Model):
    """Stores user-specific information for books, including overrides."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_books")
    quantity = models.PositiveIntegerField(default=1)

    title_override = models.CharField(max_length=255, blank=True, null=True)
    author_override = models.CharField(max_length=255, blank=True, null=True)
    isbn_override = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Item(models.Model):
    """Polymorphic model to handle different types of resources (e.g., books, other items)."""

    RESOURCE_TYPES = [
        ("book", "Book"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    resource_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.resource_type} (ID: {self.resource_id})"

    def get_resource(self):
        """Helper method to fetch the associated resource."""
        if self.resource_type == "book":
            return Book.objects.get(id=self.resource_id)


class User(models.Model):
    """Extend this model if you need additional user-specific information."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
