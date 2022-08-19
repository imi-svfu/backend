from django.contrib.auth.models import User, Group
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        ModelSerializer)

from .models import Page, Question


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        exclude = ['permissions']


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']


class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
