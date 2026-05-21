from django.contrib import admin
from .models import Building, Floor, Room, Notification, ChangeLog

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['number', 'building']
    list_filter = ['building']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'floor']
    list_filter = ['floor__building']
    filter_horizontal = ['keepers']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']

@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'model_name', 'created_at']
    list_filter = ['model_name']
