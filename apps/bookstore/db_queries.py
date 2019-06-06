from django.db.models import Prefetch
from apps.bookstore.decorators import query_debugger
from apps.bookstore.models import Book, Store


@query_debugger
def book_list():
    """ 1
    Function :  book_list
    Number of Queries : 101
    Finished in : 0.08s
    """
    queryset = Book.objects.all()

    books = []

    for book in queryset:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})

    return books


@query_debugger
def book_list_select_related():

    """ 2
    Function :  book_list_select_related
    Number of Queries : 1
    Finished in : 0.02s
    """
    queryset = Book.objects.select_related('publisher').all()

    books = []

    for book in queryset:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})

    return books


@query_debugger
def store_list():
    """ 3
    Function :  store_list
    Number of Queries : 11
    Finished in : 0.02s
    """
    queryset = Store.objects.all()

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_prefetch_related():
    """ 4
    Function : store_list_prefetch_related
    Number of Queries : 2
    Finished in : 0.01s
    """
    queryset = Store.objects.prefetch_related('books')

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_expensive_books_prefetch_related():
    """ 5
    Function :  store_list_expensive_books_prefetch_related
    Number of Queries : 12
    Finished in : 0.05s
    """
    queryset = Store.objects.prefetch_related('books')

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.filter(price__range=(250, 300))]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores


@query_debugger
def store_list_expensive_books_prefetch_related_efficient():
    """ 6
    Function :  store_list_expensive_books_prefetch_related_efficient
    Number of Queries : 2
    Finished in : 0.03s
    """
    queryset = Store.objects.prefetch_related(Prefetch('books', queryset=Book.objects.filter(price__range=(250, 300))))

    stores = []

    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return stores