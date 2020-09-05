import logging
import sqlparse
from django.core.management.base import BaseCommand
from django.db.models import Max, Count
from faker import factory

from apps.blog.models import Blog, Entry, Author, Comment
from apps.blog.tests.factories import AuthorFactory, BlogFactory, EntryFactory, CommentFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        Blog.objects.all().delete()
        Entry.objects.all().delete()
        Author.objects.all().delete()
        Comment.objects.all().delete()

        # blogs = BlogFactory.create_batch(10)
        # authors = AuthorFactory.create_batch(2)

        known_authors = [AuthorFactory(name='iamrobert'), AuthorFactory()]
        e1 = EntryFactory.create(authors=known_authors)
        e2 = EntryFactory.create(authors=known_authors)
        e3 = EntryFactory.create(authors=AuthorFactory.create_batch(2))

        CommentFactory(entry=e1)
        CommentFactory(entry=e1)
        CommentFactory(entry=e3)


