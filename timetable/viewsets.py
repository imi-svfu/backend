from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import datetime

from .models import Schedule, Lesson, Event, Group, Lecturer, Room
from rest_framework.viewsets import ModelViewSet
from .serializers import ScheduleSerializer, LessonSerializer, EventSerializer, GroupSerializer, LecturerSerializer, RoomSerializer
from rest_framework.permissions import BasePermission
from . import utils


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [BasePermission]

    def perform_create(self, serializer):
        print(self.request.data['room'])
        serializer.save (room=Room.objects.get(pk=self.request.data['room']),
                         lesson=Lesson.objects.get(pk=self.request.data['lesson']))

    def perform_update(self, serializer):
        serializer.save(room=Room.objects.get(pk=self.request.data['room']),
                        lesson=Lesson.objects.get(pk=self.request.data['lesson']))

    @action(detail=False, methods=['get'])
    def group(self, request):
        group = request.GET['id']
        schedules = Schedule.objects.filter(lesson__group__id=group)
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)



class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [BasePermission]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = Lesson.objects.filter(group__id=group)
        return queryset

    @action(detail=False, methods=['get'])
    def hours(self, request):
        group = request.GET['group_id']
        hours = []
        lessons = Lesson.objects.filter(group__id=group)
        for lesson in lessons:
            lec_events = Event.objects.filter(schedule__lesson=lesson, schedule__type='LEC')
            pra_events = Event.objects.filter(schedule__lesson=lesson, schedule__type='PRA')
            lab_events = Event.objects.filter(schedule__lesson=lesson, schedule__type='LAB')
            lec_events_count = lec_events.count()
            pra_events_count = pra_events.count()
            lab_events_count = lab_events.count()
            hours.append({
                'lesson_id': lesson.id,
                'lec': lec_events_count * 2,
                'pra': pra_events_count * 2,
                'lab': lab_events_count * 2
            })
            print(lesson)
        print(hours)
        return Response(hours)


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

    @action(detail=False, methods=['get'])
    def get_available(self, request):
        group_id = request.query_params.get('group_id')
        week_day = int(request.query_params.get('week_day'))
        pair_num = int(request.query_params.get('pair_num'))
        repeat_option = int(request.query_params.get('repeat_option'))

        rooms = utils.get_available_rooms(group_id, week_day, pair_num, repeat_option)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

