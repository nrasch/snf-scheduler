from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('snf/', views.list_snfs, name='list_snfs'),
    path('delete-snf/', views.delete_snf, name='delete_snf'),
    path('add-snf/', views.add_snf, name='add_snf'),
    path('get-snf/', views.get_snf, name='get_snf'),
    path('edit-snf/', views.edit_snf, name='edit_snf'),
    path('patient/', views.list_patients, name='list_patients'),
    path('delete-patient/', views.delete_patient, name='delete_patient'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('get-patient/', views.get_patient, name='get_patient'),
]