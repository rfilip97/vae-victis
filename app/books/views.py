from rest_framework import permissions
from rest_framework.views import APIView
from .use_cases.item import DeleteItem, UpdateItem, GetItem
from .use_cases.items import GetItems, AddItem
from .use_cases.books import ScanBook


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


class ItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return GetItems.perform(request.user, request.GET)

    def post(self, request):
        return AddItem.perform(request.user, request.data)


class ScanBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return ScanBook.perform(request.GET.get("isbn", None))
