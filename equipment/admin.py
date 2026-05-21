from django.contrib import admin
from .models import Equipment, EquipmentType, WriteOffRequest

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['reg_number', 'brand', 'model', 'room', 'condition', 'is_present', 'cost']
    list_filter = ['condition', 'equipment_type', 'is_present']
    search_fields = ['reg_number', 'brand', 'model']

@admin.register(WriteOffRequest)
class WriteOffAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'created_by', 'created_at']
