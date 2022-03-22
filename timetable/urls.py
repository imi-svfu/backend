from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ScheduleViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls))
]