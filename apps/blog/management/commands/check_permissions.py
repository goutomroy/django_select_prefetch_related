import logging
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=3)
        # logger.info(f"add: {user.has_perm('archive.add_archive')} change: {user.has_perm('archive.change_archive')} "
        #             f"view: {user.has_perm('archive.view_archive')}")
        for each in user.get_all_permissions():
            logger.info(each)
        #
        # content_type = ContentType.objects.get_for_model(Archive)
        # permission = Permission.objects.create(codename='can_publish', name='Can Publish book', content_type=content_type)
        # permission = Permission.objects.get(codename='can_publish')
        # user.user_permissions.add(permission)
        # perm_tuple = [(x.id, x.name) for x in user.user_permissions.all()]
        # logger.info(f"user permission : {perm_tuple}")