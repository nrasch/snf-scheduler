from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('home/', views.home, name='home'),

    path('snf/list', views.list_snfs, name='list_snfs'),
    path('snf/delete/', views.delete_snf, name='delete_snf'),
    path('snf/add/', views.add_snf, name='add_snf'),
    path('snf/<int:pk>/', views.get_snf, name='get_snf'),
    path('snf/edit/<int:pk>/', views.edit_snf, name='edit_snf'),

    path('patient/list', views.list_patients, name='list_patients'),
    path('patient/delete/', views.delete_patient, name='delete_patient'),
    path('patient/add/', views.add_patient, name='add_patient'),
    path('patient/<int:pk>/', views.get_patient, name='get_patient'),
    path('patient/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
]