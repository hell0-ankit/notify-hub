from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationSettingViewSet,
    NotificationLogViewSet,
    TriggerDispatchViewSet,
)

router = DefaultRouter()
router.register(r'settings', NotificationSettingViewSet, basename='notification-settings')
router.register(r'logs', NotificationLogViewSet, basename='notification-logs')
router.register(r'dispatch', TriggerDispatchViewSet, basename='dispatch')

urlpatterns = [
    path('', include(router.urls)),
]