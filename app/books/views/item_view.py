from rest_framework import permissions
from rest_framework.views import APIView
from books.use_cases.item import DeleteItem, UpdateItem, GetItem


class ItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        return DeleteItem.perform(user=request.user, item_id=item_id)

    def put(self, request, item_id):
        return UpdateItem.perform(
            user=request.user, item_id=item_id, params=request.data
        )

    def get(self, request, item_id):
        return GetItem.perform(user=request.user, item_id=item_id)
