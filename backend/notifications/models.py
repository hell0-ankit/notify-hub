from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TriggerType(models.TextChoices):
    LOGIN = 'login', 'Login'
    LOGOUT = 'logout', 'Logout'
    INACTIVITY = 'inactivity', 'Inactivity'

class ChannelType(models.TextChoices):
    WHATSAPP = 'whatsapp', 'WhatsApp'
    EMAIL = 'email', 'Email'

class NotificationSetting(models.Model):
    """Stores the trigger-channel active status and customizable templates."""
    trigger = models.CharField(max_length=30, choices=TriggerType.choices)
    channel = models.CharField(max_length=30, choices=ChannelType.choices)
    is_active = models.BooleanField(default=True)
    template_subject = models.CharField(max_length=255, blank=True, null=True, help_text="Email subject")
    template_body = models.TextField(help_text="Supports dynamic placeholders like {{name}}, {{time}}, {{site}}")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('trigger', 'channel')

    def __str__(self):
        return f"{self.trigger} - {self.channel} ({'ACTIVE' if self.is_active else 'INACTIVE'})"

class NotificationLog(models.Model):
    """Audit log tracking notification delivery results across all channels."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    trigger = models.CharField(max_length=30)
    channel = models.CharField(max_length=30)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    response_payload = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.status.upper()}] {self.trigger} via {self.channel} -> {self.recipient}"