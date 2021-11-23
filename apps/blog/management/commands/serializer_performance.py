import cProfile
import profile
from django.core.management.base import BaseCommand
from typing import Dict, Any
from django.contrib.auth.models import User
from rest_framework import serializers
from apps.bookstore.decorators import time_counter


def serialize_user(user: User) -> Dict[str, Any]:
    return {
        'id': user.id,
        'last_login': user.last_login.isoformat() if user.last_login is not None else None,
        'is_superuser': user.is_superuser,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'date_joined': user.date_joined.isoformat(),
    }


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined']


class UserReadOnlyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined']
        read_only_fields = fields


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    last_login = serializers.DateTimeField()
    is_superuser = serializers.BooleanField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    date_joined = serializers.DateTimeField()


class UserReadOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class Command(BaseCommand):

    counter = 10000

    @time_counter
    def manual_serialization(self, user):
        for i in range(self.counter):
            serialize_user(user)

    @time_counter
    def modelserializer_serialization(self, user):
        for i in range(self.counter):
            UserModelSerializer(user).data

    @time_counter
    def modelserializer_serialization_readonly(self, user):
        for i in range(self.counter):
            UserReadOnlyModelSerializer(user).data

    @time_counter
    def regular_serialization(self, user):
        for i in range(self.counter):
            UserSerializer(user).data

    @time_counter
    def regular_serialization_readonly(self, user):
        for i in range(self.counter):
            UserReadOnlySerializer(user).data

    def do_job(self):
        user = User.objects.get(username='goutom')
        self.manual_serialization(user)
        self.regular_serialization(user)
        self.regular_serialization_readonly(user)
        self.modelserializer_serialization(user)
        self.modelserializer_serialization_readonly(user)

    def handle(self, *args, **options):
        self.do_job()
        # cProfile.run('self.do_job()')
        # cProfile.runctx('do_job()', None, locals())
        # cProfile.runctx('self.do_job()', globals(), locals(), filename=None, sort='tottime')



