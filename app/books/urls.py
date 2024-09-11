from django.urls import path
from . import views

urlpatterns = [
    path("scan/", views.ScanBookView.as_view(), name="scan_book"),
    path("items/", views.ItemView.as_view(), name="items"),
    path("items/<int:item_id>", views.ItemDetailView.as_view(), name="item_details"),
]
