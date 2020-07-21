import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from apps.bookstore.models import Publisher, Store, Book, Author
from apps.bookstore.tests.factories import UserFactory


class Command(BaseCommand):
    """
    This command is for inserting Publisher, Book, Store into database.
    Insert 5 Publishers, 100 Books, 10 Stores.
    """

    def handle(self, *args, **options):
        User.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()

        # create 5 publishers
        publishers = [Publisher(name=f"Publisher{index}") for index in range(1, 6)]
        Publisher.objects.bulk_create(publishers)

        # create 20 books for every publishers and one author for each book
        counter = 0
        for publisher in Publisher.objects.all():
            for i in range(20):
                counter = counter + 1
                book = Book.objects.create(name=f"Book{counter}", price=random.randint(50, 300), publisher=publisher)
                author = Author.objects.create(user=UserFactory(), age=random.randint(20, 80))
                book.authors.set([author])

        # create 10 stores and insert 10 books in every store
        books = list(Book.objects.all())
        for i in range(10):
            temp_books = [books.pop(0) for i in range(10)]
            store = Store.objects.create(name=f"Store{i+1}")
            store.books.set(temp_books)
            store.save()




