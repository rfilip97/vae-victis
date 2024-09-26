from books.models import Item, UserBook
from rest_framework.response import Response
from rest_framework import status


def get_item_for_user(user, item_id):
    try:
        return Item.objects.get(id=item_id, user=user)
    except Item.DoesNotExist:
        return None


def get_user_book(user, item):
    resource = item.get_resource()
    try:
        return UserBook.objects.get(user=user, book=resource)
    except UserBook.DoesNotExist:
        return None


def item_data_from(item, user_book):
    return {
        "id": item.id,
        "isbn": user_book.book.isbn,
        "title": user_book.title_override or user_book.book.title,
        "author": user_book.author_override or user_book.book.author,
        "thumbnail": user_book.book.image_url,
        "quantity": user_book.quantity,
    }


class GetItem:
    @staticmethod
    def perform(user, item_id):
        item = get_item_for_user(user, item_id)
        if not item:
            return Response(
                {"error": "Item not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user_book = get_user_book(user, item)
        if not user_book:
            return Response(
                {"error": "No such user-book association found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(item_data_from(item, user_book), status=status.HTTP_200_OK)
