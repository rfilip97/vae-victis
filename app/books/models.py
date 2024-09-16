from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"[{self.isbn}] {self.title} by {self.author}"


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_books")
    quantity = models.PositiveIntegerField(default=1)

    title_override = models.CharField(max_length=255, blank=True, null=True)
    author_override = models.CharField(max_length=255, blank=True, null=True)
    isbn_override = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        title = self.title_override or self.book.title
        author = self.author_override or self.book.author
        isbn = self.isbn_override or self.book.isbn

        return f"{self.user.username} - [quantity: {self.quantity}] {title} by {author} (ISBN: {isbn})"


class Item(models.Model):
    RESOURCE_TYPES = [
        ("book", "Book"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    resource_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.resource_type} (ID: {self.resource_id})"

    def get_resource(self):
        if self.resource_type == "book":
            return Book.objects.get(id=self.resource_id)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
