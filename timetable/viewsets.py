from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.parsers import BaseParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .utils import schedule_to_excel, export_to_ical
from .utils.events import get_week_events as events_get_week_events
from .utils.pairs_begin_end import pairtime_begin, pairtime_end
from .models import Event, Group, Lecturer, Lesson, Room, Schedule, Semester
from .serializers import (ScheduleSerializer, LessonSerializer, EventSerializer,
                          GroupSerializer, LecturerSerializer, RoomSerializer)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        response = Response({'message': exc.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return response


class ICalParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/calendar'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


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
        schedule_to_excel.export()
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
        return events_get_week_events(request)


class EventViewSet2(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [BasePermission]
    parser_classes = [ICalParser]

    def list(self, request, *args, **kwargs):
        cal = export_to_ical.export(request)
        return Response(cal.to_ical(), status=status.HTTP_200_OK)
        # return Response({"msg": "dsadas"})

    # @action(detail=False, methods=['get'])
    # def export_ical(self, request):


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [BasePermission]


class LecturerViewSet(ModelViewSet):
    queryset = Lecturer.objects.order_by('name')
    serializer_class = LecturerSerializer
    permission_classes = [BasePermission]


def get_event_date_and_weeks_count(group_id, week_day):
    """ На выход дает:
    - event_date - стартовую дату event-а
    - weeks_count - количество недель в семестре
    """
    semester = Semester.objects.get(group_id=group_id)
    semester_begin = semester.study_start
    semester_end = semester.study_end

    startpoint_date = semester_begin - timedelta(days=1)
    if startpoint_date < semester_begin:
        startpoint_date = semester_begin

    if startpoint_date.isoweekday() > week_day:
        days = 7 - startpoint_date.isoweekday()
        event_date = startpoint_date + \
            timedelta(days=days) + \
            timedelta(days=week_day)
    else:
        event_date = startpoint_date + timedelta(
            days=(week_day - startpoint_date.isoweekday()))

    weeks_count = (semester_end - event_date).days // 7 + 1
    return event_date, weeks_count


def available_rooms(group_id, week_day, pair_num, repeat_option):
    rooms = Room.objects.all()

    event_date, weeks_count = get_event_date_and_weeks_count(group_id, week_day)

    if repeat_option == 0:
        step = 1
    else:
        step = 2

    week_num = event_date.isocalendar().week
    if (repeat_option == 1 and week_num % 2 == 0) or \
            (repeat_option == 2 and week_num % 2 == 1):
        event_date += timedelta(days=7)

    for i in range(0, weeks_count, step):
        base_date = event_date + timedelta(days=7 * i)
        begin = datetime.combine(base_date, pairtime_begin[pair_num])
        end = datetime.combine(base_date, pairtime_end[pair_num])
        events = Event.objects.filter(
            Q(schedule__common=0),
            Q(begin__range=(begin, end)) | Q(end__range=(begin, end))
        )
        events = events.exclude(room__num="Дист")
        rooms = rooms.exclude(event__in=events)

    return rooms


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

        rooms = available_rooms(group_id, week_day, pair_num, repeat_option)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)
