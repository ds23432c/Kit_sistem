from django.contrib import admin
from .models import RepairRequest, ChangeRequest

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ['number', 'room', 'status', 'priority', 'created_by', 'created_at']
    list_filter = ['status', 'priority']

@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['room', 'request_type', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'request_type']
