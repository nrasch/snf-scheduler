from django.db import models
import datetime

# Create your models here.
class SNF(models.Model):
    name = models.CharField(max_length=100, verbose_name="SNF Name")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    address = models.TextField(verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

class Patient(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
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
    date = models.DateTimeField(verbose_name="Appointment Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    @property
    def title(self):
        return f"{self.patient.name} at {self.snf.name} on {self.date:%Y-%m-%d}"

    def __str__(self):
        return self.title

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