from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('floors/', views.floor_list, name='floor_list'),
    path('floors/<int:pk>/', views.floor_detail, name='floor_detail'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/create-keeper/', views.create_keeper, name='create_keeper'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('changelog/', views.changelog, name='changelog'),
    path('api/notifications/count/', views.notifications_count_api, name='notifications_count_api'),
]
