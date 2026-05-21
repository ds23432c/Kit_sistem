from django.urls import path
from . import views
urlpatterns = [
    path('', views.accounting_view, name='accounting'),
    path('export/', views.accounting_export, name='accounting_export'),
    path('writeoffs/', views.writeoff_list, name='writeoff_list'),
    path('writeoff-export/', views.writeoff_export, name='writeoff_export'),
    path('1c-export/', views.export_1c, name='export_1c'),
    path('update-cost/', views.update_cost, name='update_cost'),
]
