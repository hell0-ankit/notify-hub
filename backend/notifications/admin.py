from django.contrib import admin
from .models import NotificationSetting, NotificationLog

@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'channel', 'is_active', 'updated_at')
    list_filter = ('trigger', 'channel', 'is_active')
    search_fields = ('template_subject', 'template_body')

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'trigger', 'channel', 'recipient', 'status')
    list_filter = ('status', 'channel', 'trigger', 'created_at')
    search_fields = ('recipient', 'subject', 'body', 'user__username')
    readonly_fields = [field.name for field in NotificationLog._meta.fields]