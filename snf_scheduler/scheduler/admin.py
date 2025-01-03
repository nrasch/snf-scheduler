from django.contrib import admin

# Register your models here.
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote

admin.site.register(SNF)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(AppointmentNote)
admin.site.register(PatientNote)
