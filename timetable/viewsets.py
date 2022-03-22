from .models import Schedule, Lesson, Event
from rest_framework.viewsets import ModelViewSet
from .serializers import ScheduleSerializer, LessonSerializer, EventSerializer
from rest_framework.permissions import BasePermission

"""Группа, Дата и время занятия, Название занятия, Аудитория"""


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [BasePermission]


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [BasePermission]


class EventViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = EventSerializer
    permission_classes = [BasePermission]
