from django.contrib import admin
from apps.bookstore.models import Publisher, Store, Book

admin.site.register(Book)
admin.site.register(Store)
admin.site.register(Publisher)
