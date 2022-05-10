from django.core.management.base import BaseCommand, CommandError

from timetable.models import *
from timetable.enigma import get_plan


class Command(BaseCommand):
    help = 'Import lessons from plan'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)
        parser.add_argument('groupname', nargs=1, type=str)

    def handle(self, *args, **options):
        plan = get_plan(options['filename'][0])
        """Номер семестра заполняемых занятий"""
        sem = 6
        group_name = options['groupname'][0]
        try :
            group_id = Group.objects.get(name=group_name).id
        except Group.DoesNotExist:
            raise CommandError('Не существует группы с названием "%s"' % group_name)
        semester_id = Semester.objects.get(Q(group_id=group_id) & Q(num=sem)).id
        subjects = plan.subject_codes
        for subject in subjects.items():
            optional = False
            if ".ДВ." in subject[1].code:
                optional = True
            if sem in subject[1].semesters:
                lesson = Lesson(group_id=group_id,
                                subject=subject[1].name,
                                semester_id=semester_id,
                                lectures=subject[1].semesters[sem].lectures,
                                practices=subject[1].semesters[sem].practices,
                                labs=subject[1].semesters[sem].labworks,
                                optional=optional
                                )
                lesson.save()

        self.stdout.write(self.style.SUCCESS('Successfully parsed "'))
