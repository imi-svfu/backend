from rest_framework.serializers import ModelSerializer

from .models import Page, Question


class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
