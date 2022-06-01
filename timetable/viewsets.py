from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from . import utils
from .models import Schedule, Lesson, Event, Group, Lecturer, Room
from .serializers import ScheduleSerializer, LessonSerializer, EventSerializer, GroupSerializer, LecturerSerializer, \
    RoomSerializer

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        response = Response({'message': exc.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return response

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [BasePermission]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(room=Room.objects.get(pk=self.request.data['room']),
                            lesson=Lesson.objects.get(pk=self.request.data['lesson']))
            transaction.set_rollback(True)

    def perform_update(self, serializer):
        serializer.save(room=Room.objects.get(pk=self.request.data['room']),
                        lesson=Lesson.objects.get(pk=self.request.data['lesson']))

    @action(detail=False, methods=['get'])
    def group(self, request):
        try:
            group = request.GET['id']
            schedules = Schedule.objects.filter(lesson__group__id=group)
        except (KeyError, ValueError):
            return Response([])
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exportgroup(self, request):
        group = self.request.query_params.get('group')
        utils.schedule_to_excel()
        return Response({'data': 'Таблица сформирована'}, status.HTTP_200_OK)


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
        hours = []
        try:
            group = request.GET['group_id']
            lessons = Lesson.objects.filter(group__id=group)
        except (KeyError, ValueError):
            return Response(hours)

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
        print(request.GET.get('get_by'))
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
