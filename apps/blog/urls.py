from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from .views import EntryViewSet, AuthorViewSet, CommentViewSet

app_name = 'blog'

router = routers.DefaultRouter()
router.register(r'entry', EntryViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'comment', CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
