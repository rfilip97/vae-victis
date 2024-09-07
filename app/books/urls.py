from django.urls import path
from . import views

urlpatterns = [
    path(
        "scan/", views.ScanBookView.as_view(), name="scan_book"
    ),  # Temp. Will be replaced by a generic /scan
]
