from django.contrib import admin
from .models import NotificationSetting, UserDevice, NotificationLog


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    pass

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    pass

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    pass