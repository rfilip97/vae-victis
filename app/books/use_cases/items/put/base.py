from books.models import Item, UserBook
from rest_framework.response import Response
from rest_framework import status


def get_item_for_user(user, item_id):
    try:
        return Item.objects.get(id=item_id, user=user)
    except Item.DoesNotExist:
        return None


def is_valid_item_type(item_type):
    return item_type == "book"


def is_valid_quantity(quantity):
    try:
        return int(quantity) >= 0
    except (ValueError, TypeError):
        return False


def get_user_book(user, item):
    resource = item.get_resource()
    try:
        return UserBook.objects.get(user=user, book=resource)
    except UserBook.DoesNotExist:
        return None


def update_user_book(user_book, data):
    user_book.title_override = data.get("title", user_book.title_override)
    user_book.author_override = data.get("author", user_book.author_override)
    user_book.isbn_override = data.get("isbn", user_book.isbn_override)
    user_book.quantity = data.get("quantity", user_book.quantity)
    user_book.save()


class AddItem:
    @staticmethod
    def perform(user, item_id, params):
        item = get_item_for_user(user, item_id)
        if not item:
            return Response(
                {"error": "Item not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )

        item_type = params.get("type")
        quantity = params.get("quantity")

        if not is_valid_item_type(item_type):
            return Response(
                {"error": "Unsupported item type"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not is_valid_quantity(quantity):
            return Response(
                {"error": "Quantity cannot be less than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_book = get_user_book(user, item)
            update_user_book(user_book, params)
            return Response(
                {"message": "Item updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
