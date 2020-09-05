from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.bookstore.models import Book, Publisher, Store


"""
# Select Related

We use select_related when the object that you're going to select is a single object, 
which means forward ForeignKey, OneToOne and backward OneToOne.
"""


@api_view(['GET'])
def forward_one_to_one_without_sr(request):
    """
    Return all the publishers with associated owner, without using select_related.

    61ms overall
    5ms on queries
    11 queries

    1 query to fetch all publishers:

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id"
    FROM "bookstore_publisher"

    10 separate query to fetch owner of each publisher:

    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined"
    FROM "auth_user"
    WHERE "auth_user"."id" = 1
    LIMIT 21

    """
    qs = Publisher.objects.all()
    publishers = []
    for publisher in qs:
        publishers.append({'id': publisher.id, 'username': publisher.owner.username})
    return Response(publishers)


@api_view(['GET'])
def forward_one_to_one_with_sr(request):
    """
    Return all the publishers with associated owner, using select_related.

    53ms overall
    1ms on queries
    1 queries

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id",
           "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined"
    FROM "bookstore_publisher"
    INNER JOIN "auth_user" ON ("bookstore_publisher"."owner_id" = "auth_user"."id")

    """
    qs = Publisher.objects.select_related('owner')
    publishers = []
    for publisher in qs:
        publishers.append({'id': publisher.id, 'username': publisher.owner.username})
    return Response(publishers)


@api_view(['GET'])
def backward_one_to_one_without_sr(request):
    """
    Return all the users with associated reverse publisher, without using select_related.

    106ms overall
    15ms on queries
    11 queries

    1 query to fetch all users:

    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined"
    FROM "auth_user"

    10 separate query to fetch publisher of each user:

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id"
    FROM "bookstore_publisher"
    WHERE "bookstore_publisher"."owner_id" = 1
    LIMIT 21

    """
    qs = User.objects.all()
    users = []
    for user in qs:
        users.append({'id': user.id, 'username': user.username, 'publisher': user.publisher.name})
    return Response(users)


@api_view(['GET'])
def backward_one_to_one_with_sr(request):
    """
    Return all the users with associated reverse publisher, without using select_related.

    54ms overall
    1ms on queries
    1 queries

    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined",
           "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id"
    FROM "auth_user"
    LEFT OUTER JOIN "bookstore_publisher" ON ("auth_user"."id" = "bookstore_publisher"."owner_id")

    """
    qs = User.objects.select_related('publisher')
    users = []
    for user in qs:
        users.append({'id': user.id, 'username': user.username, 'publisher': user.publisher.name})
    return Response(users)


@api_view(['GET'])
def forward_foreign_key_without_sr(request):
    """
    Return all the books with associated publisher, without using select_related.

    401ms overall
    77ms on queries
    101 queries

    1 query to fetch all books:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"

    100 separate query to fetch publisher of each book:

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id"
    FROM "bookstore_publisher"
    WHERE "bookstore_publisher"."id" = 1
    LIMIT 21

    """
    qs = Book.objects.all()
    books = []
    for book in qs:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})
    return Response(books)


@api_view(['GET'])
def forward_foreign_key_with_sr(request):
    """
    Return all the books with associated publisher, using select_related.

    92ms overall
    2ms on queries
    1 queries

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id",
           "bookstore_publisher"."id",
           "bookstore_publisher"."name",
           "bookstore_publisher"."owner_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_publisher" ON ("bookstore_book"."publisher_id" = "bookstore_publisher"."id")

    """
    qs = Book.objects.select_related('publisher')
    books = []
    for book in qs:
        books.append({'id': book.id, 'name': book.name, 'publisher': book.publisher.name})
    return Response(books)


"""
# Prefetch Related

We use prefetch_related when we’re going to get a set of things.
That means forward and backward ManyToMany, backward ForeignKey. 
prefetch_related does a separate lookup for each relationship, and performs the “joining” in Python.
It is different from select_related, the prefetch_related made the JOIN using Python rather than in the database.
"""


@api_view(['GET'])
def backward_foreign_key_without_pr(request):
    """
    Return all the publishers with associated books, without using prefetch_related.

    64ms overall
    2ms on queries
    6 queries

    1 query to fetch all publishers:

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name"
    FROM "bookstore_publisher"

    5 separate query to fetch books of each publisher:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    WHERE "bookstore_book"."publisher_id" = 16

    """
    qs = Publisher.objects.all()
    publishers = []
    for publisher in qs:
        books = [{'id': book.id, 'name': book.name} for book in publisher.books.all()]
        publishers.append({'id': publisher.id, 'name': publisher.name, 'books': books})

    return Response(publishers)


@api_view(['GET'])
def backward_foreign_key_with_pr(request):
    """
    For testing prefetch_related.
    Return all the publishers with associated books, using prefetch_related.

    60ms overall
    2ms on queries
    2 queries

    1 query to fetch all publishers:

    SELECT "bookstore_publisher"."id",
           "bookstore_publisher"."name"
    FROM "bookstore_publisher"

    Another query to fetch all the books of publishers, then django does pythonic join of these 2 queries to populate result:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    WHERE "bookstore_book"."publisher_id" IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    """
    qs = Publisher.objects.prefetch_related('books')
    publishers = []
    for publisher in qs:
        books = [{'id': book.id, 'name': book.name} for book in publisher.books.all()]
        publishers.append({'id': publisher.id, 'name': publisher.name, 'books': books})

    return Response(publishers)


@api_view(['GET'])
def forward_many_to_many_without_pr(request):
    """
    Return all the stores with associated books, without using prefetch_related.

    100ms overall
    8ms on queries
    11 queries

    1 query to fetch all stores:

    SELECT "bookstore_store"."id",
           "bookstore_store"."name"
    FROM "bookstore_store"

    10 separate query to fetch books of each store:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
    WHERE "bookstore_bookinstore"."store_id" = 1

    """
    qs = Store.objects.all()
    stores = []
    for store in qs:
        books = [{'id': book.id, 'name': book.name} for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return Response(stores)


@api_view(['GET'])
def forward_many_to_many_with_pr(request):
    """
    Return all the stores with associated books, using prefetch_related.

    95ms overall
    4ms on queries
    2 queries

    1 query to fetch all stores:

    SELECT "bookstore_store"."id",
           "bookstore_store"."name"
    FROM "bookstore_store"

    Another query to fetch all the books of selected stores, then django does pythonic join of these 2 queries to populate result:

    SELECT ("bookstore_bookinstore"."store_id") AS "_prefetch_related_val_store_id",
           "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
    WHERE "bookstore_bookinstore"."store_id" IN (1, 2, 3, ...)

    """
    qs = Store.objects.prefetch_related('books')
    stores = []
    for store in qs:
        books = [{'id': book.id, 'name': book.name} for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return Response(stores)


@api_view(['GET'])
def backward_many_to_many_without_pr(request):
    """
    Return all the books with associated stores, without using prefetch_related.

    286ms overall
    51ms on queries
    101 queries

    1 query to fetch all books:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"

    100 separate query to fetch stores of each book:

    SELECT "bookstore_store"."id",
           "bookstore_store"."name"
    FROM "bookstore_store"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_store"."id" = "bookstore_bookinstore"."store_id")
    WHERE "bookstore_bookinstore"."book_id" = 1

    """
    qs = Book.objects.all()
    books = []
    for book in qs:
        stores = [{'id': store.id, 'name': store.name} for store in book.stores.all()]
        books.append({'id': book.id, 'name': book.name, 'stores': stores})
    return Response(books)


@api_view(['GET'])
def backward_many_to_many_with_pr(request):
    """
    Return all the books with associated stores, using prefetch_related.

    166ms overall
    4ms on queries
    2 queries

    1 query to fetch all books:

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"

    Another query to fetch stores of each book, then django does pythonic join of these 2 queries to populate result:

    SELECT ("bookstore_bookinstore"."book_id") AS "_prefetch_related_val_book_id",
           "bookstore_store"."id",
           "bookstore_store"."name"
    FROM "bookstore_store"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_store"."id" = "bookstore_bookinstore"."store_id")
    WHERE "bookstore_bookinstore"."book_id" IN (1, 2, 3, ...)

    """
    qs = Book.objects.prefetch_related('stores')
    books = []
    for book in qs:
        stores = [{'id': store.id, 'name': store.name} for store in book.stores.all()]
        books.append({'id': book.id, 'name': book.name, 'stores': stores})
    return Response(books)


@api_view(['GET'])
def stores_expensive_books_pr(request):

    """
    Return all stores with expensive books.

    72ms overall
    7ms on queries
    12 queries

    SELECT "bookstore_store"."id",
           "bookstore_store"."name"
    FROM "bookstore_store"

    SELECT ("bookstore_bookinstore"."store_id") AS "_prefetch_related_val_store_id",
           "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
    WHERE "bookstore_bookinstore"."store_id" IN (41, 42, 43, 44, 45, 46, 47, 48, 49, 50)

    More 10 queries as below :

    SELECT "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
    WHERE ("bookstore_bookinstore"."store_id" = 41
           AND "bookstore_book"."price" BETWEEN 250 AND 300)


    Despite the fact that we are using prefetch_related, our queries increased rather than decreased. But why?
    Using prefetch related, we are telling Django to give all the results to be JOINED, but when we use the filter(price__range=(250, 300)),
    we are changing the primary query and then Django doesn’t JOIN the right results for us.

    Let’s solve the problem with Prefetch.

    """

    queryset = Store.objects.prefetch_related('books')
    stores = []
    for store in queryset:
        books = [book.name for book in store.books.filter(price__range=(250, 300))]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return Response(stores)


@api_view(['GET'])
def stores_expensive_books_pr_efficient(request):

    """
    Return all stores with expensive books.

    63ms overall
    3ms on queries
    2 queries

    SELECT "bookstore_store"."id", "bookstore_store"."name"
    FROM "bookstore_store"

    SELECT ("bookstore_bookinstore"."store_id") AS "_prefetch_related_val_store_id",
           "bookstore_book"."id",
           "bookstore_book"."name",
           "bookstore_book"."price",
           "bookstore_book"."publisher_id"
    FROM "bookstore_book"
    INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
    WHERE ("bookstore_book"."price" BETWEEN 250 AND 300
           AND "bookstore_bookinstore"."store_id" IN (41, 42, 43, 44, 45, 46, 47, 48, 49, 50))
    """

    queryset = Store.objects.prefetch_related(Prefetch('books', queryset=Book.objects.filter(price__range=(250, 300))))

    stores = []
    for store in queryset:
        books = [book.name for book in store.books.all()]
        stores.append({'id': store.id, 'name': store.name, 'books': books})

    return Response(stores)