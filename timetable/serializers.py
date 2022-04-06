from rest_framework import serializers
from .models import Schedule, Event, Lesson, Semester, Subject, Group, Lecturer, Room


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    subject = SubjectSerializer()
    class Meta:
        model = Lesson
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    room = RoomSerializer()
    class Meta:
        model = Event
        fields = '__all__'


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'
