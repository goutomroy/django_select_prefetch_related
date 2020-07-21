from rest_framework import serializers
from apps.bookstore.models import Book, Publisher, Store


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class BookSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    books = BookSerializerNested(many=True)

    class Meta:
        model = Store
        fields = '__all__'