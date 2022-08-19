from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Page, Question
from .serializers import PageSerializer, QuestionSerializer


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
