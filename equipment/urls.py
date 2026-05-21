from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('add/', views.equipment_add, name='equipment_add'),
    path('<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('<int:pk>/writeoff/', views.equipment_writeoff, name='equipment_writeoff'),
    path('import/', views.equipment_import, name='equipment_import'),
    path('export/', views.equipment_export, name='equipment_export'),
    path('template/', views.download_template, name='equipment_template'),
]
