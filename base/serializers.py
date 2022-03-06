from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        exclude = ['permissions']
