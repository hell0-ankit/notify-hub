from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .models import NotificationSetting, NotificationLog, UserDevice
from .serializers import NotificationSettingSerializer, NotificationLogSerializer
from .engine import dispatch_trigger

User = get_user_model()

class NotificationSettingViewSet(viewsets.ModelViewSet):
    queryset = NotificationSetting.objects.all().order_by('trigger', 'channel')
    serializer_class = NotificationSettingSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Toggle active state of a trigger-channel",
        request=inline_serializer(
            name='ToggleChannelRequest',
            fields={
                'trigger': serializers.CharField(),
                'channel': serializers.CharField(),
                'is_active': serializers.BooleanField(),
            }
        ),
        responses={200: NotificationSettingSerializer}
    )
    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle_channel(self, request):
        trigger = request.data.get('trigger')
        channel = request.data.get('channel')
        is_active = request.data.get('is_active')

        if not trigger or not channel or is_active is None:
            return Response(
                {"error": "trigger, channel, and is_active are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        setting, _ = NotificationSetting.objects.get_or_create(trigger=trigger, channel=channel)
        setting.is_active = bool(is_active)
        setting.save()
        return Response(NotificationSettingSerializer(setting).data)


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationLog.objects.all().order_by('-created_at')
    serializer_class = NotificationLogSerializer
    permission_classes = [AllowAny]


class DeviceRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Register user device OneSignal subscription ID",
        request=inline_serializer(
            name='RegisterDeviceRequest',
            fields={
                'player_id': serializers.CharField(),
                'user_id': serializers.IntegerField(required=False),
            }
        ),
        responses={200: dict}
    )
    def create(self, request):
        player_id = request.data.get('player_id')
        user_id = request.data.get('user_id')

        if not player_id:
            return Response({"error": "player_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first() if user_id else User.objects.first()
        if not user:
            return Response({"error": "No user available to associate this device."}, status=status.HTTP_400_BAD_REQUEST)

        device, _ = UserDevice.objects.get_or_create(user=user, player_id=player_id)
        return Response({"message": "Device registered successfully.", "device_id": device.id})


class TriggerDispatchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Manually trigger an event (login, logout, inactivity)",
        request=inline_serializer(
            name='TriggerDispatchRequest',
            fields={
                'trigger': serializers.ChoiceField(choices=['login', 'logout', 'inactivity']),
                'user_id': serializers.IntegerField(required=False),
            }
        ),
        responses={200: dict}
    )
    def create(self, request):
        trigger_name = request.data.get('trigger')
        user_id = request.data.get('user_id')

        if not trigger_name:
            return Response({"error": "trigger is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first() if user_id else User.objects.first()
        if not user:
            return Response({"error": "No user available to receive the trigger."}, status=status.HTTP_400_BAD_REQUEST)

        dispatch_trigger(user=user, trigger_event=trigger_name)
        return Response({
            "message": f"Trigger '{trigger_name}' executed for user '{user.username}'."
        })