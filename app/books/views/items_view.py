from rest_framework import permissions
from rest_framework.views import APIView
from books.use_cases.items import GetItems, AddItem


class ItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return GetItems.perform(request.user, request.GET)

    def post(self, request):
        return AddItem.perform(request.user, request.data)
