import datetime
import os
from django.db import models
from rest_framework import request


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @property
    def url(self):
        return 'author/' + str(self.id)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(blank=True, null=True)

    class Meta:
        default_related_name = 'blogs'
        permissions = [
            ("change_name", "Can change the name of the blog")]

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    authors = models.ManyToManyField(Author, blank=True)
    headline = models.CharField(max_length=255)
    body_text = models.TextField(blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    mod_date = models.DateField(blank=True, null=True)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    class Meta:
        default_related_name = 'entries'

    def __str__(self):
        return self.headline + " " + str(self.pub_date)

    @property
    def url(self):
        return 'entry/' + str(self.id)


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, blank=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

