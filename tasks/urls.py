from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SpecialTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'special-tasks', SpecialTaskViewSet, basename='special-task')

urlpatterns = [
    path('', include(router.urls)),
]
