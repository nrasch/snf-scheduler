from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from scheduler.models import SNF, Patient, Appointment, AppointmentNote, PatientNote

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        # Create some SNFs
        for i in range(3):
            SNF.objects.create(
                name=f"SNF {i+1}",
                description=f"This is SNF number {i+1}",
                address=f"Address {i+1}"
            )

        # Create some patients
        first_names = ["John", "Jane", "Mike", "Emily", "David"]
        last_names = ["Doe", "Smith", "Johnson", "Brown", "Wilson"]
        for i in range(5):
            birth_date = timezone.now().date() - timedelta(days=random.randint(365*18, 365*80))
            Patient.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                date_of_birth=birth_date,
                date_of_last_appointment=None,
                date_of_next_appointment=None,
                active=True
            )

        # Create some appointments
        snfs = SNF.objects.all()
        patients = Patient.objects.all()
        for i in range(10):
            appointment_date = timezone.now() + timedelta(days=random.randint(1, 30))
            Appointment.objects.create(
                snf=random.choice(snfs),
                patient=random.choice(patients),
                date=appointment_date
            )

        # Add notes to some appointments
        for appointment in Appointment.objects.all():
            if random.choice([True, False]):  # 50% chance to add a note
                AppointmentNote.objects.create(
                    appointment=appointment,
                    text=f"Note for appointment {appointment.id}"
                )

        # Add notes to some patients
        for patient in Patient.objects.all():
            if random.choice([True, False]):  # 50% chance to add a note
                PatientNote.objects.create(
                    patient=patient,
                    text=f"Note for patient {patient.id}"
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))