from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root),
    path('snfs/', views.SNFListCreate.as_view(), name='snf-list-create'),
    path('snfs/<int:pk>/', views.SNFDetail.as_view(), name='snf-detail'),
    path('patients/', views.PatientListCreate.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetail.as_view(), name='patient-detail'),
    path('appointments/', views.AppointmentListCreate.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-detail'),
    path('appointment-notes/', views.AppointmentNoteListCreate.as_view(), name='appointment-notes-list-create'),
    path('appointment-notes/<int:pk>/', views.AppointmentNoteDetail.as_view(), name='appointments-note-detail'),
    path('patient-notes/', views.PatientNoteListCreate.as_view(), name='patient-notes-list-create'),
    path('patient-notes/<int:pk>/', views.PatientNoteDetail.as_view(), name='patient-notes-detail'),
]
