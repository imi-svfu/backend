from rest_framework import serializers
from .models import Schedule, Lesson, Event


class ScheduleSerializer(serializers.ModelSerializer):
    lesson = serializers.ReadOnlyField(source='lesson.subject.name')

    class Meta:
        model = Schedule
        fields = ['id', 'week_day', 'pair_num', 'lesson', 'type', 'room', 'repeat_option', 'common']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
