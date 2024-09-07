from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Book, UserBook, Item


class BooksModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.book1 = Book.objects.create(
            title="Dune",
            author="Frank Herbert",
            image_url="http://example.com/dune.jpg",
            isbn="9780441013593",
        )
        self.book2 = Book.objects.create(
            title="1984",
            author="George Orwell",
            image_url="http://example.com/1984.jpg",
            isbn="9780451524935",
        )

        self.user_book1 = UserBook.objects.create(
            user=self.user,
            book=self.book1,
            quantity=1,
            title_override=None,
            author_override=None,
            isbn_override=None,
        )
        self.user_book2 = UserBook.objects.create(
            user=self.user,
            book=self.book2,
            quantity=1,
            title_override=None,
            author_override=None,
            isbn_override=None,
        )

        self.item1 = Item.objects.create(
            user=self.user, resource_type="book", resource_id=self.book1.id
        )
        self.item2 = Item.objects.create(
            user=self.user, resource_type="book", resource_id=self.book2.id
        )

    def test_books_are_created(self):
        """Test that books are correctly created."""
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(self.book1.title, "Dune")
        self.assertEqual(self.book2.title, "1984")

    def test_user_books_are_created(self):
        """Test that user books are correctly created."""
        self.assertEqual(UserBook.objects.count(), 2)
        self.assertEqual(self.user_book1.book.title, "Dune")
        self.assertEqual(self.user_book2.book.title, "1984")
        self.assertEqual(self.user_book1.user.username, "testuser")

    def test_items_are_created(self):
        """Test that items are correctly created for books."""
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(self.item1.get_resource().title, "Dune")
        self.assertEqual(self.item2.get_resource().title, "1984")

    def test_nested_relationship_access(self):
        """Test that nested access from items to user_books and book works."""
        item = self.user.items.first()
        user_book = UserBook.objects.filter(book_id=item.resource_id).first()
        book_title = user_book.book.title

        self.assertEqual(book_title, "Dune")
