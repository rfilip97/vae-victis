from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from books.models import Book, UserBook, Item


class AddItemTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.book = Book.objects.create(
            isbn="9786067580648",
            title="Dune   - Editura Nemira",
            author="Frank Herbert",
            image_url="http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )

    def test_add_item_success(self):
        data = {
            "type": "book",
            "isbn": "9786067580648",
            "title": "Dune   - Editura Nemira",
            "author": "Frank Herbert",
            "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        }

        response = self.client.post(reverse("items"), data)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(UserBook.objects.count(), 1)

        user_book = UserBook.objects.first()
        self.assertEqual(user_book.book.isbn, "9786067580648")
        self.assertEqual(user_book.user, self.user)

    def test_add_item_duplicate(self):
        UserBook.objects.create(user=self.user, book=self.book)

        data = {
            "type": "book",
            "isbn": "9786067580648",
            "title": "Dune   - Editura Nemira",
            "author": "Frank Herbert",
            "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        }

        response = self.client.post(reverse("items"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], "This book has already been added to your items."
        )

    def test_add_item_unsupported_type(self):
        data = {
            "type": "movie",
            "isbn": "9786067580648",
            "title": "Dune   - Editura Nemira",
            "author": "Frank Herbert",
            "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        }

        response = self.client.post(reverse("items"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Unsupported item type")

    def test_add_item_no_book_found(self):
        data = {
            "type": "book",
            "isbn": "1234567890123",
            "title": "Some Other Book",
            "author": "Some Author",
            "thumbnail": "http://example.com/thumbnail.jpg",
        }

        response = self.client.post(reverse("items"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], "Book not found. Please scan the book first."
        )


class GetUserItemsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.book1 = Book.objects.create(
            isbn="9786067580648",
            title="Dune   - Editura Nemira",
            author="Frank Herbert",
            image_url="http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )

        self.book2 = Book.objects.create(
            isbn="9780141981802",
            title="Life 3.0",
            author="Max Tegmark",
            image_url="http://books.google.com/books/content?id=aDj9EAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )

        self.user_book1 = UserBook.objects.create(
            user=self.user,
            book=self.book1,
            title_override="Dune - Custom Edition",
            author_override=None,
            isbn_override=None,
        )
        Item.objects.create(
            user=self.user,
            resource_type="book",
            resource_id=self.book1.id,
        )

        self.user_book2 = UserBook.objects.create(
            user=self.user,
            book=self.book2,
            title_override=None,
            author_override="Custom Author",
            isbn_override=None,
        )
        Item.objects.create(
            user=self.user,
            resource_type="book",
            resource_id=self.book2.id,
        )

    def test_get_user_items(self):
        response = self.client.get(reverse("items"))

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "id": 2,
                "isbn": "9786067580648",
                "title": "Dune - Custom Edition",
                "author": "Frank Herbert",
                "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "quantity": 1,
            },
            {
                "id": 3,
                "isbn": "9780141981802",
                "title": "Life 3.0",
                "author": "Custom Author",
                "thumbnail": "http://books.google.com/books/content?id=aDj9EAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "quantity": 1,
            },
        ]

        self.assertEqual(response.json(), expected_response)

    def test_get_user_items_no_items(self):
        Item.objects.filter(user=self.user).delete()
        UserBook.objects.filter(user=self.user).delete()

        response = self.client.get(reverse("items"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_user_items_unauthenticated(self):
        self.client.credentials()

        response = self.client.get(reverse("items"))

        self.assertEqual(response.status_code, 401)
