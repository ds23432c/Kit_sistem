from django.urls import path
from . import views
urlpatterns = [
    path('', views.map_view, name='map'),
    path('editor/', views.map_editor, name='map_editor'),
    path('api/floor/<int:pk>/save/', views.save_floor_map, name='save_floor_map'),
    path('api/room/<int:pk>/info/', views.room_info_api, name='room_info_api'),
]
