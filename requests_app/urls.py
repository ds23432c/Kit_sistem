from django.urls import path
from . import views
urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('new/', views.request_create, name='request_create'),
    path('<int:pk>/update-status/', views.request_update_status, name='request_update_status'),
    path('<int:pk>/download/', views.request_download_docx, name='request_download_docx'),
    path('change-requests/', views.change_request_list, name='change_request_list'),
    path('change-requests/new/', views.change_request_create, name='change_request_create'),
    path('change-requests/<int:pk>/review/', views.change_request_review, name='change_request_review'),
]
