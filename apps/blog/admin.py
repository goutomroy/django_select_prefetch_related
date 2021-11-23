from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from apps.blog.models import Blog, Author, Entry, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    readonly_fields = ['id']


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tagline', 'number_of_entries')
    readonly_fields = ['id']

    def number_of_entries(self, obj):
        return str(obj.entries.count())


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_id', 'blog', 'headline', 'number_of_authors', 'name_of_authors', 'rating', 'pub_date')
    readonly_fields = ['id']
    list_filter = ['blog', 'pub_date']

    def number_of_authors(self, obj):
        return str(obj.authors.count())

    def name_of_authors(self, obj):
        names = '-'.join([each.name for each in obj.authors.all()])
        return names


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry_id', 'entry_headline', 'likes')
    readonly_fields = ['id', 'entry_headline']

    def entry_headline(self, obj):
        return obj.entry.headline


admin.site.register(Author, AuthorAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(ContentType)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Country)
