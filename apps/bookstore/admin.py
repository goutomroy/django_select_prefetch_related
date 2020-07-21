from django.contrib import admin
from apps.bookstore.models import Publisher, Store, Book, Author, BookInStore

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Store)
admin.site.register(BookInStore)

