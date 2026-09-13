from django.contrib import admin
from .models import Trigger, NotificationTemplate


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'trigger',
        'channel',
        'is_enabled',
        'created_at',
    )
    list_filter = ('channel', 'is_enabled')