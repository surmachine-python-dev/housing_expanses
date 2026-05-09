from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete/<int:pk>/', views.delete_reading, name='delete_reading'),
    path('edit/<int:pk>/', views.edit_reading, name='edit_reading'),
    path('fee/delete/<int:pk>/', views.delete_fee_rate, name='delete_fee_rate'),
    path('fee/edit/<int:pk>/', views.edit_fee_rate, name='edit_fee_rate'),
]
