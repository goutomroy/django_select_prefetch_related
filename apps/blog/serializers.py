import os

from rest_framework import serializers
from .models import Entry, Author, Comment, Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'name', 'tagline')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name', 'email', 'url')


class EntrySerializer(serializers.ModelSerializer):
    blog = BlogSerializer()
    authors = AuthorSerializer(many=True)
    # d = serializers.URLField(source='url', read_only='True')

    class Meta:
        model = Entry
        fields = ['id', 'blog', 'headline', 'body_text', 'authors', 'url']

    # def get_absolute_url(self):
    #     domain = Site.objects.get_current().domain
    #     path = os.path.join(domain, 'author/'+str(self.id))
    #     print(path)
    #     return path

    # get_sr_price = serializers.SerializerMethodField('get_sr_price_func')
    #
    # def get_absolute_url(self, obj):
    #     return os.path.join(self.get_serializer_context['request'].get_host(), 'author/'+str(self.id))


class CommentSerializer(serializers.ModelSerializer):

    entry = EntrySerializer()

    class Meta:
        model = Comment
        fields = ('id', 'entry', 'text', 'likes')