from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Schedule, Lesson, Event, Group, Lecturer, Room
from rest_framework.viewsets import ModelViewSet
from .serializers import ScheduleSerializer, LessonSerializer, EventSerializer, GroupSerializer, LecturerSerializer, RoomSerializer
from rest_framework.permissions import BasePermission
from . import utils


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [BasePermission]

    @action(detail=False, methods=['get'])
    def group(self, request):
        group = request.GET['id']
        schedules = Schedule.objects.filter(lesson__group__id=group)
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [BasePermission]


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [BasePermission]

    @action(detail=False, methods=['get'])
    def get_week_events(self, request):
        print(request.GET['get_by'])
        return utils.get_week_events(self, request)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [BasePermission]


class LecturerViewSet(ModelViewSet):
    queryset = Lecturer.objects.order_by('name')
    serializer_class = LecturerSerializer
    permission_classes = [BasePermission]


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.order_by('num')
    serializer_class = RoomSerializer
    permission_classes = [BasePermission]
