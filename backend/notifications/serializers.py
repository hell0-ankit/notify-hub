from rest_framework import serializers
from .models import NotificationSetting, NotificationLog, UserDevice

class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = ['id', 'trigger', 'channel', 'is_active', 'template_subject', 'template_body', 'updated_at']

class NotificationLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default='N/A')

    class Meta:
        model = NotificationLog
        fields = ['id', 'username', 'trigger', 'channel', 'recipient', 'subject', 'body', 'status', 'response_payload', 'created_at']

class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['id', 'player_id', 'created_at']