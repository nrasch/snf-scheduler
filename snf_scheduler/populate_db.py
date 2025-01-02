from django.core.management.base import BaseCommand
from scheduler.models import SNF, Patient, Appointment

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        snf = SNF.objects.create(name="Test SNF", description="Sample SNF")
        patient = Patient.objects.create(first_name="Jane", last_name="Smith", date_of_birth="1985-05-05")
        Appointment.objects.create(snf=snf, patient=patient, date="2025-01-01 12:00:00")
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))