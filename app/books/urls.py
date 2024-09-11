from django.urls import path
from . import views

urlpatterns = [
    path("scan/", views.ScanBookView.as_view(), name="scan_book"),
    path("item/", views.ItemView.as_view(), name="item"),
]
