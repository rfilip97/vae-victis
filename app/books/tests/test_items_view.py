from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from books.models import Book, UserBook, Item


class ItemDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass"
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.book = Book.objects.create(
            isbn="9786067580648",
            title="Dune   - Editura Nemira",
            author="Frank Herbert",
            image_url="http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )

        self.item = Item.objects.create(
            user=self.user, resource_type="book", resource_id=self.book.id
        )
        self.user_book = UserBook.objects.create(
            user=self.user,
            book=self.book,
            title_override="Dune: Special Edition",
            author_override="Frank Herbert Jr.",
            quantity=1,
        )

    def test_delete_item_success(self):
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(UserBook.objects.count(), 1)

        response = self.client.delete(
            reverse("item_details", kwargs={"item_id": self.item.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Item deleted successfully")

        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(UserBook.objects.count(), 0)

    def test_delete_item_not_found(self):
        response = self.client.delete(reverse("item_details", kwargs={"item_id": 999}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "Item not found or does not belong to you"
        )

    def test_delete_item_unauthorized_access(self):
        other_book = Book.objects.create(
            isbn="9780143111597",
            title="The Catcher in the Rye",
            author="J.D. Salinger",
            image_url="http://books.google.com/books/content?id=catcher-in-the-rye&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        other_item = Item.objects.create(
            user=self.other_user, resource_type="book", resource_id=other_book.id
        )
        UserBook.objects.create(
            user=self.other_user,
            book=other_book,
            title_override=None,
            author_override=None,
            isbn_override=None,
            quantity=1,
        )

        response = self.client.delete(
            reverse("item_details", kwargs={"item_id": other_item.id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "Item not found or does not belong to you"
        )

    def test_delete_item_without_authentication(self):
        self.client.credentials()

        response = self.client.delete(
            reverse("item_details", kwargs={"item_id": self.item.id})
        )

        self.assertEqual(response.status_code, 401)

    def test_get_item_success(self):
        response = self.client.get(reverse("item_details", args=[self.item.id]))

        self.assertEqual(response.status_code, 200)

        expected_data = {
            "id": self.item.id,
            "isbn": "9786067580648",
            "title": "Dune: Special Edition",
            "author": "Frank Herbert Jr.",
            "thumbnail": self.book.image_url,
            "quantity": 1,
        }

        self.assertEqual(response.json(), expected_data)

    def test_get_item_not_found(self):
        response = self.client.get(reverse("item_details", args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "Item not found or does not belong to you"
        )

    def test_get_item_no_user_book_association(self):
        self.user_book.delete()

        response = self.client.get(reverse("item_details", args=[self.item.id]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "No such user-book association found")

    def test_update_item_success(self):
        data = {
            "type": "book",
            "title": "Updated Title",
            "author": "Frank Herbert Jr.",
            "isbn": "9786067580648",
            "quantity": 2,
        }

        response = self.client.put(
            reverse("item_details", kwargs={"item_id": self.item.id}), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Item updated successfully")

        self.user_book.refresh_from_db()
        self.assertEqual(self.user_book.title_override, "Updated Title")
        self.assertEqual(self.user_book.author_override, "Frank Herbert Jr.")
        self.assertEqual(self.user_book.isbn_override, "9786067580648")
        self.assertEqual(self.user_book.quantity, 2)

    def test_update_item_invalid_type(self):
        data = {
            "type": "movie",
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "9786067580648",
            "quantity": 1,
        }

        response = self.client.put(
            reverse("item_details", kwargs={"item_id": self.item.id}), data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Unsupported item type")

    def test_update_item_invalid_quantity(self):
        data = {
            "type": "book",
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "9786067580648",
            "quantity": -1,
        }

        response = self.client.put(
            reverse("item_details", kwargs={"item_id": self.item.id}), data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Quantity cannot be less than 0")

    def test_update_item_not_found(self):
        data = {
            "type": "book",
            "title": "Dune",
            "author": "Frank Herbert",
            "isbn": "9786067580648",
            "quantity": 1,
        }

        response = self.client.put(
            reverse("item_details", kwargs={"item_id": 999}), data
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"], "Item not found or does not belong to you"
        )


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
        self.book_item_1 = Item.objects.create(
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
        self.book_item_2 = Item.objects.create(
            user=self.user,
            resource_type="book",
            resource_id=self.book2.id,
        )

    def test_get_user_items(self):
        response = self.client.get(reverse("items"))

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "id": self.book_item_1.id,
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

    def test_get_user_items_search_query(self):
        response = self.client.get(reverse("items"), {"search": "dune"})

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                "id": self.book_item_1.id,
                "isbn": "9786067580648",
                "title": "Dune - Custom Edition",
                "author": "Frank Herbert",
                "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
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
