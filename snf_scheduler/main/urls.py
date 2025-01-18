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

    path('patient/', views.list_patients, name='list_patients'),
    path('delete-patient/', views.delete_patient, name='delete_patient'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('get-patient/', views.get_patient, name='get_patient'),
    path('edit-patient/', views.edit_patient, name='edit_patient'),
]