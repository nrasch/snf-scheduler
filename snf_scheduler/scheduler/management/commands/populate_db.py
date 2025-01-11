from django.core.management.base import BaseCommand
from datetime import timedelta, datetime
from holidays import US
from django.utils import timezone
import random
from scheduler.models import SNF, Patient, Appointment, AppointmentNote, PatientNote

class Command(BaseCommand):
    help = 'Populate the database with test data'

    # Define SNFs with their details which we'll use later on to setup appointments, etc.
    snfs = {
        "Rapid City Regional Hospital SNF": {
            "description": "A comprehensive skilled nursing facility associated with Rapid City Regional Hospital, offering post-acute care and rehabilitation services.",
            "hour_opens": "08:00",
            "hour_closes": "17:00",
            "max_concurrent_appointments": 3,
            "address": "567 Oak Street, Rapid City, SD 57701",
            "phone": "(605) 345-6789"
        },
        "Black Hills Care Center": {
            "description": "Specializing in long-term care and rehabilitation, this center is nestled in the scenic Black Hills, providing a comforting environment for recovery.",
            "hour_opens": "09:00",
            "hour_closes": "18:00",
            "max_concurrent_appointments": 4,
            "address": "123 Pine Avenue, Rapid City, SD 57702",
            "phone": "(605) 987-6543"
        },
        "Pine Haven Nursing Home": {
            "description": "Located amidst pine forests, Pine Haven offers personalized care with a focus on comfort and community for its residents.",
            "hour_opens": "08:00",
            "hour_closes": "17:00",
            "max_concurrent_appointments": 2,
            "address": "456 Cedar Lane, Rapid City, SD 57703",
            "phone": "(605) 789-0123"
        },
        "Rushmore Rehabilitation Center": {
            "description": "Near Mount Rushmore, this center provides specialized rehabilitation programs for patients aiming for recovery and improved mobility.",
            "hour_opens": "09:00",
            "hour_closes": "18:00",
            "max_concurrent_appointments": 3,
            "address": "789 Summit Road, Rapid City, SD 57704",
            "phone": "(605) 234-5678"
        },
        "Canyon Hills Skilled Nursing": {
            "description": "Canyon Hills combines skilled nursing with the natural beauty of the Black Hills, offering short and long-term care options.",
            "hour_opens": "08:00",
            "hour_closes": "17:00",
            "max_concurrent_appointments": 4,
            "address": "321 Boulder Way, Rapid City, SD 57705",
            "phone": "(605) 456-7890"
        }
    }

    def handle(self, *args, **options):
        # Create some SNFs
        snf_names = list(self.snfs.keys())
        for snf in snf_names:
            SNF.objects.create(
                name=snf,
                description=self.snfs[snf]["description"],
                address=self.snfs[snf]["address"],
                phone=self.snfs[snf]["phone"],
                hour_opens=self.snfs[snf]["hour_opens"],
                hour_closes=self.snfs[snf]["hour_closes"],
                max_concurrent_appointments=self.snfs[snf]["max_concurrent_appointments"]
            )

        # Create patients
        first_names = ["John", "Jane", "Mike", "Emily", "David", "Sarah", "Tom", "Lisa", "Mark", "Anna", "Paul",
                       "Sophie", "Brian", "Emma", "Kevin", "Olivia", "Chris", "Megan", "Steve", "Ava"]
        last_names = ["Doe", "Smith", "Johnson", "Brown", "Wilson", "Taylor", "Anderson", "Thomas", "Jackson", "White",
                      "Harris", "Martin", "Thompson", "Moore", "Allen", "Young", "Lewis", "Walker", "Hall", "King"]

        for fname, lname in zip(first_names, last_names):
            # Generate a birth date that ensures the person is not older than 75
            birth_date = timezone.now().date() - timedelta(days=random.randint(365 * 18, 365 * 75))
            Patient.objects.create(
                first_name=fname,
                last_name=lname,
                date_of_birth=birth_date,
                date_of_last_appointment=None,
                date_of_next_appointment=None,
                active=True
            )

        # Function to check if a date is a weekday and not a US holiday
        # This is also defined in model validators
        def is_valid_visit_date(date):
            us_holidays = US(years=date.year)
            return date.weekday() < 5 and date not in us_holidays

        # Create appointments for the patients at the SNFs
        snfs = SNF.objects.all()
        for patient in Patient.objects.all():
            # Choose one SNF for each patient
            snf = random.choice(snfs)

            # Determine number of visits between 6 and 15
            num_visits = random.randint(6, 15)

            # Start date in 2014, ensuring it's not on a weekend or holiday
            start_date = datetime(2014, 1, 1)
            while not is_valid_visit_date(start_date):
                start_date += timedelta(days=1)

            for i in range(num_visits):
                # Calculate visit date, ensuring 30 days apart
                visit_date = start_date + timedelta(days=30 * i)

                # Adjust if the calculated date falls on a non-valid day
                while not is_valid_visit_date(visit_date):
                    visit_date += timedelta(days=1)

                # Generate a valid time for the visit within the SNF's operating hours
                # Convert time to hours for the operation
                opens_hour = snf.hour_opens.hour
                closes_hour = snf.hour_closes.hour

                # Ensure we don't go beyond the closing hour
                hour = random.randint(opens_hour, closes_hour - 1)

                # Construct a datetime object for the visit
                visit_datetime = datetime(visit_date.year, visit_date.month, visit_date.day, hour)

                # Create the appointment
                Appointment.objects.create(
                    snf=snf,
                    patient=patient,
                    date=visit_datetime,
                    duration=timedelta(hours=1)  # Visits last 1 hour
                )

        # Add notes to some appointments
        for appointment in Appointment.objects.all():
            if random.choice([True, False]):  # 50% chance to add a note
                AppointmentNote.objects.create(
                    appointment=appointment,
                    text=f"Test note for appointment {appointment.id}"
                )

        # Add notes to some patients
        for patient in Patient.objects.all():
            if random.choice([True, False]):  # 50% chance to add a note
                PatientNote.objects.create(
                    patient=patient,
                    text=f"Test note for patient {patient.id}"
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))