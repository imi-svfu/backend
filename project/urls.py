from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from base import views as base_views
from base.viewsets import PageViewSet, QuestionViewSet
from timetable.viewsets import (
    ScheduleViewSet, LessonViewSet, EventViewSet, EventViewSet2, GroupViewSet,
    LecturerViewSet, RoomViewSet
)

router = routers.DefaultRouter()
router.register('pages', PageViewSet)
router.register('questions', QuestionViewSet)
router.register('schedules', ScheduleViewSet)
router.register('lessons', LessonViewSet, 'lesson-list')
router.register('events', EventViewSet)
router.register('ical', EventViewSet2)
router.register('groups', GroupViewSet)
router.register('lecturers', LecturerViewSet)
router.register('rooms', RoomViewSet)

urlpatterns = [
    path('', base_views.index_page),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('timetable/', include('timetable.urls')),
]
