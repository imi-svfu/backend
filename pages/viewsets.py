from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Page
from .serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
