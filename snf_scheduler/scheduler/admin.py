from django.contrib import admin
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote

# Register your models here.
admin.site.register(SNF)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(AppointmentNote)
admin.site.register(PatientNote)

