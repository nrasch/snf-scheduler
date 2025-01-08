from django.core.exceptions import ValidationError
from datetime import datetime
import holidays
#from .models import Appointment


class CustomValidators:
    @staticmethod
    def validate_holiday(value):
        if value in holidays.US():
            raise ValidationError("Date cannot be a holiday.")

    @staticmethod
    def validate_not_weekend(value):
        if value.weekday() >= 5:
            raise ValidationError("Date cannot be a weekend.")

    @staticmethod
    def validate_unique_appointment(snf_id, patient_id, date):
        print("snf_id: ", snf_id)
        print("patient_id: ", patient_id)
        print("date: ", date)
        from .models import Appointment  # Lazy import inside the function to avoid circular imports
        existing_appointments = Appointment.objects.filter(
            snf=snf_id,
            patient=patient_id,
            date__date=date.date()
        )
        print("existing_appointments: ", existing_appointments)
        if existing_appointments.exists():
            print("existing_appointments.exists()")
            raise ValidationError("This appointment already exists for the patient at that SNF on that date.")