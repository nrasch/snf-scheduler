from django.db import models
import datetime
from .validators import CustomValidators

# Create your models here.
class SNF(models.Model):
    name = models.CharField(max_length=100, verbose_name="SNF Name")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    address = models.TextField(verbose_name="Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number", default="000-000-0000")
    hour_opens = models.TimeField(verbose_name="Opening Hour", default=datetime.time(8, 0), error_messages={'required': "Opening hour is required."})
    hour_closes = models.TimeField(verbose_name="Closing Hour", default=datetime.time(17, 0), error_messages={'required': "Closing hour is required."})
    max_concurrent_appointments = models.PositiveIntegerField(default=0, verbose_name="Maximum Concurrent Appointments")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

class Patient(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    #address = models.TextField(verbose_name="Address")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    date_of_last_appointment = models.DateField(null=True, blank=True, verbose_name="Last Appointment Date")
    date_of_next_appointment = models.DateField(null=True, blank=True, verbose_name="Next Appointment Date")
    active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    @property
    def age(self):
        return int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    snf = models.ForeignKey(SNF, on_delete=models.CASCADE, verbose_name="Associated SNF")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient")
    date = models.DateTimeField(verbose_name="Appointment Date",
                                validators=[CustomValidators.validate_holiday, CustomValidators.validate_not_weekend])
    duration = models.DurationField(verbose_name="Appointment Duration", default=datetime.timedelta(hours=1))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    @property
    def title(self):
        return f"{self.patient.name} at {self.snf.name} on {self.date:%Y-%m-%d %H:%M %p}"

    def __str__(self):
        return self.title

    def clean(self):
        # Ensure we don't have a duplicate appointment for the same patient at the same SNF on the same date
        CustomValidators.validate_unique_appointment(self.snf.id, self.patient.id, self.date)


class AppointmentNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Appointment")
    text = models.TextField(verbose_name="Note Text")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.text[:50]

class PatientNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient")
    text = models.TextField(verbose_name="Note Text")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.text[:50]