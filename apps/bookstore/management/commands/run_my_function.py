from django.core.management.base import BaseCommand
from apps.bookstore.db_queries import book_list, book_list_select_related, store_list, \
    store_list_prefetch_related, \
    store_list_expensive_books_prefetch_related, store_list_expensive_books_prefetch_related_efficient


class Command(BaseCommand):

    def handle(self, *args, **options):
        # book_list()
        # book_list_select_related()
        # store_list()
        store_list_prefetch_related()
        # store_list_expensive_books_prefetch_related()
        # store_list_expensive_books_prefetch_related_efficient()




