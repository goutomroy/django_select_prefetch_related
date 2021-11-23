from django.shortcuts import render
from rest_framework import viewsets, generics, request
from rest_framework.decorators import api_view

from apps.blog.serializers import EntrySerializer, AuthorSerializer, CommentSerializer
from apps.blog.models import Entry, Author, Comment


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class EntryViewSet(viewsets.ModelViewSet):

    queryset = Entry.objects.select_related('blog').prefetch_related('authors')
    serializer_class = EntrySerializer

    # def get_serializer(self, *args, **kwargs):
    #     """
    #     Return the serializer instance that should be used for validating and
    #     deserializing input, and for serializing output.
    #     """
    #     serializer_class = self.get_serializer_class()
    #     kwargs['context'] = self.get_serializer_context()
    #     return serializer_class(*args, **kwargs)
    #
    #
    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        robert = Author.objects.get(name='iamrobert')
        qs = Comment.objects.filter(entry__authors=robert)
        qs = qs.select_related('entry__blog').prefetch_related('entry__authors')
        return qs


# @api_view(['GET'])
# def checking_sr_pr(request):
#
#     """
#     Return all stores with expensive books.
#
#     72ms overall
#     7ms on queries
#     12 queries
#
#     SELECT "bookstore_store"."id",
#            "bookstore_store"."name"
#     FROM "bookstore_store"
#
#     SELECT ("bookstore_bookinstore"."store_id") AS "_prefetch_related_val_store_id",
#            "bookstore_book"."id",
#            "bookstore_book"."name",
#            "bookstore_book"."price",
#            "bookstore_book"."publisher_id"
#     FROM "bookstore_book"
#     INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
#     WHERE "bookstore_bookinstore"."store_id" IN (41, 42, 43, 44, 45, 46, 47, 48, 49, 50)
#
#     More 10 queries as below :
#
#     SELECT "bookstore_book"."id",
#            "bookstore_book"."name",
#            "bookstore_book"."price",
#            "bookstore_book"."publisher_id"
#     FROM "bookstore_book"
#     INNER JOIN "bookstore_bookinstore" ON ("bookstore_book"."id" = "bookstore_bookinstore"."book_id")
#     WHERE ("bookstore_bookinstore"."store_id" = 41
#            AND "bookstore_book"."price" BETWEEN 250 AND 300)
#
#
#     Despite the fact that we are using prefetch_related, our queries increased rather than decreased. But why?
#     Using prefetch related, we are telling Django to give all the results to be JOINED, but when we use the filter(price__range=(250, 300)),
#     we are changing the primary query and then Django doesn’t JOIN the right results for us.
#
#     Let’s solve the problem with Prefetch.
#
#     """
#
#     queryset = Store.objects.prefetch_related('books')
#     stores = []
#     for store in queryset:
#         books = [book.name for book in store.books.filter(price__range=(250, 300))]
#         stores.append({'id': store.id, 'name': store.name, 'books': books})
#
#     return Response(stores)