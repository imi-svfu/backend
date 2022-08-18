from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import ScheduleViewSet, LessonViewSet, EventViewSet, EventViewSet2, GroupViewSet, LecturerViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'lessons', LessonViewSet, 'lesson-list')
router.register(r'events', EventViewSet)
router.register(r'ical', EventViewSet2)
router.register(r'groups', GroupViewSet)
router.register(r'lecturers', LecturerViewSet)
router.register(r'rooms', RoomViewSet)

app_name = 'timetable'

urlpatterns = [
    path('base/', views.index_page, name='index_page'),
    path('', include(router.urls))
]
