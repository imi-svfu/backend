from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ScheduleViewSet, LessonViewSet, EventViewSet, GroupViewSet, LecturerViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'lessons', LessonViewSet, 'lesson-list')
router.register(r'events', EventViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'lecturers', LecturerViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls))
]