from books.models import Item, UserBook
from rest_framework.response import Response
from rest_framework import status


class DeleteItem:
    @staticmethod
    def perform(user, item_id):
        try:
            item = Item.objects.get(id=item_id, user=user)
            resource = item.get_resource()
            user_book = UserBook.objects.get(user=user, book=resource)

            user_book.delete()
            item.delete()

            return Response(
                {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
            )

        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except UserBook.DoesNotExist:
            return Response(
                {"error": "User-book association not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
