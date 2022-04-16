from django.db import models
from django.db.models import Q

from . import utils


class Event(models.Model):
    begin = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Конец")
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Тип", default="Учебное занятие", max_length=255)
    schedule = models.ForeignKey('Schedule', verbose_name="График занятий", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.type} {self.lesson}'

    def save(self, *args, **kwargs):
        errors = []
        queryset_by_room = Event.objects.filter(Q(room__id=self.room.id),
                                                Q(begin__range=(self.begin, self.end)) | Q(
                                                    end__range=(self.begin, self.end)))

        if queryset_by_room.exists():
            errors.append(f"Данная аудитория в это время занята, идет событие {queryset_by_room[0]}")

        queryset_by_group = Event.objects.filter(Q(lesson__group__id=self.lesson.group.id),
                                                 Q(begin__range=(self.begin, self.end)) | Q(
                                                     end__range=(self.begin, self.end)))
        if queryset_by_group.exists() and self.lesson.group.num != "Дистанционно":
            errors.append("Данная группа в это время занята")

        queryset_by_lecturer = Event.objects.filter(Q(lesson__lecturer__id=self.lesson.lecturer.id),
                                                    Q(begin__range=(self.begin, self.end)) | Q(
                                                        end__range=(self.begin, self.end)))
        if queryset_by_lecturer.exists():
            errors.append("Преподаватель в это время есть другое занятие")

        if errors:
            raise Exception(errors)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class Lesson(models.Model):
    group = models.ForeignKey('Group', verbose_name='Группа', on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='Дисциплина', max_length=255)
    lecturer = models.ForeignKey('Lecturer', verbose_name='Преподаватель', on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey('Semester', verbose_name='Семестр', on_delete=models.RESTRICT)
    optional = models.BooleanField(verbose_name='Выборочный', default=False)
    lectures = models.SmallIntegerField(verbose_name='Часы лекционных заянятий', null=True)
    practices = models.SmallIntegerField(verbose_name='Часы практических', null=True)
    labs = models.SmallIntegerField(verbose_name='Часы лабораторных занятий', null=True)

    def __str__(self):
        return f"{self.group} {self.subject} "

    class Meta:
        verbose_name = "Учебное занятие"
        verbose_name_plural = "Учебные занятия"
        ordering = ["group", "subject"]


class Schedule(models.Model):
    LECTURE = 'LEC'
    PRACTICE = 'PRA'
    LABORATORY = 'LAB'

    TYPE_CHOICES = [
        (LECTURE, 'Лекция'),
        (PRACTICE, 'Практика'),
        (LABORATORY, 'Лабораторная'),
    ]

    EACH = 0
    ODD = 1
    EVEN = 2

    REPEAT_OPTION_CHOICES = [
        (EACH, 'Каждую неделю'),
        (ODD, 'По нечетным'),
        (EVEN, 'По четным')
    ]

    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7

    WEEK_DAY_CHOICES = [
        (MON, 'Понедельник'),
        (TUE, 'Вторник'),
        (WED, 'Среда'),
        (THU, 'Четверг'),
        (FRI, 'Пятница'),
        (SAT, 'Суббота'),
        (SUN, 'Воскресенье'),
    ]

    lesson = models.ForeignKey('Lesson', verbose_name="Учебное занятие", on_delete=models.CASCADE, null=True)
    type = models.CharField(verbose_name="Тип", max_length=3, choices=TYPE_CHOICES, default=LECTURE)
    room = models.ForeignKey('Room', verbose_name="Кабинет", on_delete=models.CASCADE)
    pair_num = models.SmallIntegerField(verbose_name="Номер пары")
    week_day = models.SmallIntegerField(verbose_name="День недели", choices=WEEK_DAY_CHOICES)
    repeat_option = models.SmallIntegerField(verbose_name="Параметр повторения", choices=REPEAT_OPTION_CHOICES,
                                             default=EACH)
    common = models.BooleanField(verbose_name="Потоковое занятие", default=False)

    def __str__(self):
        return f"{self.lesson} {self.week_day} {self.pair_num} {self.repeat_option}"

    def save(self, *args, **kwargs):
        try:
            utils.generate_events(self)
            super().save(*args, **kwargs)
        except Exception as e:
            raise e

    class Meta:
        verbose_name = "График занятия"
        verbose_name_plural = "Графики занятий"
        # ordering = ["week_day", "pair_num"]


class Semester(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    num = models.SmallIntegerField(verbose_name="Номер")
    study_start = models.DateField(verbose_name="Начало обучения")
    study_end = models.DateField(verbose_name="Конец обучения")
    exams_start = models.DateField(verbose_name="Начало сессии")
    exams_end = models.DateField(verbose_name="Конец сессии")

    def __str__(self):
        return f"{self.num} семестр {self.group}"

    class Meta:
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"


class Group(models.Model):
    name = models.CharField(verbose_name="Название группы", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Room(models.Model):
    num = models.CharField(verbose_name="Номер", max_length=50)

    def __str__(self):
        return self.num

    class Meta:
        verbose_name = "Кабинет"
        verbose_name_plural = "Кабинеты"
        ordering = ["num"]


class Lecturer(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["name"]
