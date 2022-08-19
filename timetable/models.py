from django.contrib import admin
from django.db.models import (
    BooleanField, CASCADE, CharField, DateField, DateTimeField, ForeignKey,
    Model, Q, RESTRICT, SET_NULL, SmallIntegerField
)

from .utils import events


class Event(Model):
    begin = DateTimeField(verbose_name="начало")
    end = DateTimeField(verbose_name="конец")
    lesson = ForeignKey('Lesson', verbose_name="дисциплина", on_delete=CASCADE,
                        null=True)
    room = ForeignKey('Room', verbose_name="аудитория", on_delete=CASCADE)
    type = CharField(verbose_name="тип", default="Учебное занятие",
                     max_length=255)
    schedule = ForeignKey('Schedule', verbose_name="график занятий",
                          on_delete=CASCADE, null=True)

    def __str__(self):
        event_str = f"{self.type} {self.lesson}"
        if self.schedule.subgroup:
            event_str += f" (1/{self.lesson.group.subgroups})"
        return event_str

    def get_room_errors(self):
        errors = []
        if self.room.num != "Дист":
            queryset_by_room = Event.objects.filter(
                Q(room__id=self.room.id),
                Q(begin__range=(self.begin, self.end)) |
                Q(end__range=(self.begin, self.end))
            )
            if queryset_by_room.exists():
                schedule_common = queryset_by_room[0].schedule.common
                if schedule_common == 0 or \
                        (schedule_common == 1 and self.schedule.common == 0):
                    errors.append(f"Данная аудитория в это время занята, "
                                  f"идет событие {queryset_by_room[0]}")
        return errors

    def get_study_group_errors(self):
        errors = []
        group_events_cur_range = Event.objects.filter(
            Q(lesson__group__id=self.lesson.group.id),
            Q(begin__range=(self.begin, self.end)) |
            Q(end__range=(self.begin, self.end))
        )
        subgroup_event = group_events_cur_range.filter(schedule__subgroup=True)
        if group_events_cur_range.exists() and not subgroup_event.exists():
            errors.append("Данная группа в это время занята")
        if self.schedule.subgroup and \
                (subgroup_event.count() >= int(self.lesson.group.subgroups)):
            errors.append("Все подгруппы заняты")
        if not self.schedule.subgroup and subgroup_event.exists():
            errors.append("В данное время есть занятия по подгруппам")
        return errors

    def get_teacher_errors(self):
        errors = []
        sport = "Элективные дисциплины по физической культуре и спорту"
        if self.lesson.subject != sport:
            queryset_by_lecturer = Event.objects.filter(
                Q(lesson__lecturer__id=self.lesson.lecturer.id),
                Q(begin__range=(self.begin, self.end)) |
                Q(end__range=(self.begin, self.end))
            )
            if queryset_by_lecturer.exists():
                if queryset_by_lecturer[0].room != self.room:
                    errors.append(f"У преподавателя в это время есть "
                                  f"занятие в другом кабинете - "
                                  f"{queryset_by_lecturer[0].room}")
        return errors

    def save(self, *args, **kwargs):
        errors = self.get_room_errors()
        errors += self.get_study_group_errors()
        errors += self.get_teacher_errors()
        if errors:
            raise Exception(errors)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"


class Lesson(Model):
    # TODO: remove redundant group, because it's available through semester
    group = ForeignKey('Group', verbose_name="группа", on_delete=CASCADE)
    subject = CharField(verbose_name="наименование", max_length=255)
    lecturer = ForeignKey('Lecturer', verbose_name="преподаватель",
                          on_delete=SET_NULL, null=True)
    semester = ForeignKey('Semester', verbose_name="семестр",
                          on_delete=RESTRICT)
    optional = BooleanField(verbose_name="по выбору", default=False)
    lectures = SmallIntegerField(verbose_name="лекции", null=True, blank=True)
    practices = SmallIntegerField(verbose_name="практики", null=True,
                                  blank=True)
    labs = SmallIntegerField(verbose_name="лаб.раб.", null=True, blank=True)

    def __str__(self):
        return f"{self.semester.group} {self.subject}"

    class Meta:
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"
        ordering = ['group', 'subject']


LECTURE = 'LEC'
PRACTICE = 'PRA'
LABORATORY = 'LAB'

NONE = 3
EACH = 0
ODD = 1
EVEN = 2

MON = 1
TUE = 2
WED = 3
THU = 4
FRI = 5
SAT = 6
SUN = 7


class Schedule(Model):
    TYPE_CHOICES = (
        (LECTURE, "Лекция"),
        (PRACTICE, "Практика"),
        (LABORATORY, "Лабораторная"),
    )

    REPEAT_OPTION_CHOICES = (
        (NONE, "Без повторов"),
        (EACH, "Каждую неделю"),
        (ODD, "По нечетным"),
        (EVEN, "По четным")
    )

    WEEK_DAY_CHOICES = (
        (MON, "Понедельник"),
        (TUE, "Вторник"),
        (WED, "Среда"),
        (THU, "Четверг"),
        (FRI, "Пятница"),
        (SAT, "Суббота"),
        (SUN, "Воскресенье"),
    )

    lesson = ForeignKey('Lesson', verbose_name="учебное занятие",
                        on_delete=CASCADE, null=True)
    type = CharField(verbose_name="тип", max_length=3, choices=TYPE_CHOICES,
                     default=LECTURE)
    room = ForeignKey('Room', verbose_name="кабинет", on_delete=CASCADE)
    pair_num = SmallIntegerField(verbose_name="номер пары")
    week_day = SmallIntegerField(verbose_name="день недели",
                                 choices=WEEK_DAY_CHOICES)
    repeat_option = SmallIntegerField(verbose_name="параметр повторения",
                                      choices=REPEAT_OPTION_CHOICES,
                                      default=EACH)
    common = BooleanField(verbose_name="потоковое занятие", default=False)
    subgroup = BooleanField(verbose_name="подгруппа", default=False)

    def __str__(self):
        result = f"{self.lesson}"
        if self.subgroup:
            result += f" (1/{self.lesson.group.subgroups})"
        result += f" {self.week_day} {self.pair_num} {self.repeat_option}"
        return result

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            events.generate(self)
        except Exception as e:
            raise e

    class Meta:
        verbose_name = "график занятия"
        verbose_name_plural = "графики занятий"
        # ordering = ['week_day', 'pair_num']


class Semester(Model):
    group = ForeignKey('Group', verbose_name="группа", on_delete=CASCADE)
    num = SmallIntegerField(verbose_name="семестр")
    study_start = DateField(verbose_name="начало обучения")
    study_end = DateField(verbose_name="конец обучения")
    exams_start = DateField(verbose_name="начало сессии")
    exams_end = DateField(verbose_name="конец сессии")

    def __str__(self):
        return f"{self.group}: {self.num} сем."

    @admin.display(description="период обучения")
    def study_period(self):
        return f"{self.study_start} – {self.study_end}"

    @admin.display(description="сессия")
    def exams_period(self):
        return f"{self.exams_start} – {self.exams_end}"

    class Meta:
        verbose_name = "период обучения"
        verbose_name_plural = "график учебного процесса"


class Group(Model):
    name = CharField(verbose_name="название группы", max_length=255)
    subgroups = SmallIntegerField(verbose_name="количество подгрупп",
                                  null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"


class Room(Model):
    num = CharField(verbose_name="номер", max_length=50)

    def __str__(self):
        return self.num

    class Meta:
        verbose_name = "аудитория"
        verbose_name_plural = "аудитории"
        ordering = ['num']


class Lecturer(Model):
    name = CharField(verbose_name="имя", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "преподаватель"
        verbose_name_plural = "преподаватели"
        ordering = ['name']
