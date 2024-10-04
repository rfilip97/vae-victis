from django.urls import path
from books.views import *

urlpatterns = [
    path("scan/", BooksView.as_view(), name="scan_book"),
    path("items/", ItemsView.as_view(), name="items"),
    path("items/<int:item_id>", ItemView.as_view(), name="item_details"),
]
