from books.models import Item, UserBook
from rest_framework.response import Response
from rest_framework import status


def is_match(resource, user_book, search_query):
    if not search_query:
        return True

    search_query = search_query.lower()

    return (
        search_query in (user_book.title_override or resource.title).lower()
        or search_query in (user_book.author_override or resource.author).lower()
    )


def item_data_from(item, resource, user_book):
    return {
        "id": item.id,
        "isbn": resource.isbn,
        "title": user_book.title_override or resource.title,
        "author": user_book.author_override or resource.author,
        "thumbnail": resource.image_url,
        "quantity": user_book.quantity,
    }


def get_items_for(user, search_query=None):
    items = Item.objects.filter(user=user)
    items_data = []

    for item in items:
        resource = item.get_resource()

        try:
            user_book = UserBook.objects.get(user=user, book=resource)
            if is_match(resource, user_book, search_query):
                items_data.append(item_data_from(item, resource, user_book))
        except UserBook.DoesNotExist:
            continue

    return items_data


class GetItems:
    @staticmethod
    def perform(user, params):
        search_query = params.get("search", None)

        return Response(get_items_for(user, search_query), status=status.HTTP_200_OK)
