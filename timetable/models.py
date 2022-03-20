from django.db import models


class Event(models.Model):
    begin = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Конец")
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Тип", default="Учебное занятие", max_length=255)

    def __str__(self):
        return self.begin

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class Lesson(models.Model):
    group = models.ForeignKey('Group', verbose_name='Группа', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', verbose_name='Дисциплина', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', verbose_name='Преподаватель', on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey('Semester',  verbose_name='Семестр', on_delete=models.RESTRICT)
    optional = models.BooleanField(verbose_name='Выборочный', default=False)
    week_day = models.SmallIntegerField(verbose_name="День недели")
    repeat_option = models.SmallIntegerField(verbose_name="Параметр повторения")
    common = models.BooleanField(verbose_name="Потоковое занятие", default=False)

    def __str__(self):
        return f"{self.subject} {self.group}"

    class Meta:
        verbose_name = "Учебное занятие"
        verbose_name_plural = "Учебные занятия"
        ordering = ["group", "week_day"]


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


class Subject(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ["name"]


class Lecturer(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
