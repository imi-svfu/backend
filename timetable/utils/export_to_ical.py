from icalendar import Calendar, Event as ical_event_class
from datetime import datetime
import os
from pathlib import Path

from timetable import models

schedule_types = {
    "LEC": "Лек",
    "PRA": "Пр",
    "LAB": "Лаб",
}

def export(request):
    group_id = request.GET.get('group_id')
    group_name = models.Group.objects.get(pk=group_id).name

    cal = Calendar()
    cal.add('prodid', '-//КИТ ИМИ СВФУ//')
    cal.add('name', f'Расписание занятий группы {group_name}')
    cal.add('version', '2.0')

    events = models.Event.objects.filter(lesson__group_id=group_id)

    for event in events:
        ical_event = ical_event_class()
        ical_event.add('summary', schedule_types[event.type])
        ical_event.add('dtstart', event.begin)
        ical_event.add('dtend', event.end)
        ical_event.add('dtstamp', datetime.now())
        ical_event.add('organizer', event.lesson.lecturer.name)
        ical_event.add('location', event.room.num)
        ical_event.add('description', event.lesson.subject)
        ical_event.add('uid', event.id)
        cal.add_component(ical_event)

    dir = Path(__file__).resolve().parent.parent.parent
    f = open(os.path.join(dir, 'schedule.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()
