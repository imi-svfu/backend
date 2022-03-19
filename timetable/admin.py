from django.contrib import admin

from . import models


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("subject", "group", "lecturer")


@admin.register(models.Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("group", "num")


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("begin", "end", "lesson", "room", "type")


admin.site.register(models.Group)
admin.site.register(models.Room)
admin.site.register(models.Subject)
admin.site.register(models.Lecturer)

