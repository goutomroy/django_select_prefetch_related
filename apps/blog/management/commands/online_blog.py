import logging
import sqlparse
from django.core.management.base import BaseCommand
from django.db.models import Max, Count
from apps.blog.models import Blog, Entry
from apps.bookstore.decorators import query_debugger
from django.db.models import CharField, Count, FloatField, Avg
from django.db.models.functions import Lower

from apps.bookstore.models import Book
from utils import print_query


class Command(BaseCommand):

    @query_debugger
    def run_query(self):
        qs = Entry.objects.all()
        # qs = Entry.objects.select_related('blog')
        # print_query(qs)
        for each in qs:
            # print(type(each.blog))
            # print(type(each.authors))
            print(each.headline)

    def inner_join(self):
        # qs = Blog.objects.filter(entries__rating__gte=4)
        qs = Blog.objects.filter(entries__rating__gte=4).values('id', 'name', 'entries__id', 'entries__headline',
                                                                'entries__rating')
        # qs = Blog.objects.all()
        print_query(qs)
        for each in qs:
            print(each)

    def left_join_1(self):
        qs = Blog.objects.values('id', 'name', 'entries__id', 'entries__headline', 'entries__rating')
        print_query(qs)
        for each in qs:
            print(each)

    def left_join_2(self):
        qs = Entry.objects.select_related('blog').values('id', 'headline', 'rating', 'blog_id', 'blog__name')
        print_query(qs)
        for each in qs:
            print(each)

    def annotation_test(self):
        # q = Book.objects.filter(publisher__name='Shroff')
        # q = Book.objects.annotate(num_authors=Count('authors'))
        q = Book.objects.aggregate(price_diff=
                                   Max('price', output_field=FloatField()) -
                                   Avg('price', output_field=FloatField()))
        logger.info(q)

    def handle(self, *args, **options):
        self.annotation_test()
        # self.run_query()
        # self.inner_join()
        # self.left_join_1()
        # self.left_join_2()


