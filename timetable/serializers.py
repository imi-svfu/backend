from rest_framework import serializers
from .models import Schedule, Event, Lesson, Semester, Group, Lecturer, Room


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    lecturer = LecturerSerializer()
    class Meta:
        model = Lesson
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    room = RoomSerializer()
    class Meta:
        model = Event
        fields = '__all__'
