from django.db import models
from django.conf import settings


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'books'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book, through='BookInStore')

    class Meta:
        default_related_name = 'stores'

    def __str__(self):
        return self.name


class BookInStore(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # default_related_name = 'store_books'
        constraints = [
            models.UniqueConstraint(fields=['book', 'store'], name='a book can be added in a store only once.')
        ]


