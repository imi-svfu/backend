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
    list_display = ("begin", "end", "lesson", "room", "type", "schedule")
    readonly_fields = ('schedule',)


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "week_day", "lesson", "type", "pair_num", "room", "repeat_option", "subgroup", "common")
    fields = ("week_day", "pair_num", "lesson", "type", "room", "repeat_option", "subgroup", "common")
    list_display_links = ("lesson",)
    list_filter = ("lesson__group", "week_day", "room")


admin.site.register(models.Group)
admin.site.register(models.Room)
admin.site.register(models.Lecturer)

