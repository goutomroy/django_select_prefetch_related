from django.contrib import admin
from apps.bookstore.models import Publisher, Store, Book, BookInStore

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Store)
admin.site.register(BookInStore)

