import datetime

from django.db.models import Q

from timetable import models

from . import pairs_begin_end
from .events import get_event_date_and_weeks_count


def get(group_id, week_day, pair_num, repeat_option):
    rooms = models.Room.objects.all()

    event_date = get_event_date_and_weeks_count.get(group_id, week_day)['start_event_date']
    weeks_count = get_event_date_and_weeks_count.get(group_id, week_day)['weeks_count']

    pairtime_begin, pairtime_end = pairs_begin_end.get(pair_num)['begin'], pairs_begin_end.get(pair_num)[
        'end']

    if repeat_option == 0:
        step = 1
    else:
        step = 2

    if (repeat_option == 1 and event_date.isocalendar().week % 2 == 0) or \
            (repeat_option == 2 and event_date.isocalendar().week % 2 == 1):
        event_date += datetime.timedelta(days=7)

    for i in range(0, weeks_count, step):
        begin = datetime.datetime.combine(event_date + datetime.timedelta(days=7 * i), pairtime_begin)
        end = datetime.datetime.combine(event_date + datetime.timedelta(days=7 * i), pairtime_end)

        events = models.Event.objects.filter(Q(schedule__common=0),
                                             Q(begin__range=(begin, end)) | Q(end__range=(begin, end)))

        events = events.exclude(room__num="Дист")

        rooms = rooms.exclude(event__in=events)

    return rooms
