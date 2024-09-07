from django.contrib import admin
from .models import Book, UserBook, Item

admin.site.register(Book)
admin.site.register(UserBook)
admin.site.register(Item)
