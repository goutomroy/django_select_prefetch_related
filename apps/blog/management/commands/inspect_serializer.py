import logging

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from rest_framework import serializers

from apps.multi_crud.serializers import ShampooSerializer

logger = logging.getLogger(__name__)


# class TaskSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Task
#         fields = ('title', 'user')
#         # fields = '__all__'


class Command(BaseCommand):

    def handle(self, *args, **options):
        # logger.info(f"serialized representation: {repr(TaskSerializer())}")
        serializer = ShampooSerializer()
        logger.info(repr(serializer))
        # user = User.objects.get(id=1)
        # task = Task.objects.get(id=16)
        # serializer = TaskSerializer(task)
        # logger.info(f"serialized data: {serializer.data}")
        # data = {'title': 'Any title'}
        # serializer = TaskSerializer(data=data)
        # if serializer.is_valid():
        #     logger.info(f"validated data: {serializer.validated_data}")
        # else:
        #     logger.info(f"validation error: {serializer.errors}")
