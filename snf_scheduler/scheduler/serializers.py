from rest_framework import serializers
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from .validators import CustomValidators
from django.core.exceptions import ValidationError

class SNFSerializer(serializers.HyperlinkedModelSerializer):
    patients = serializers.HyperlinkedRelatedField(many=True, view_name='patient-detail', read_only=True)

    class Meta:
        model = SNF
        fields = ['id', 'name', 'description', 'address', 'patients']
        read_only_fields = ['id', 'url', 'created_at', 'updated_at']

class PatientNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PatientNote
        fields = ['id', 'text']
        read_only_fields = ['id', 'url', 'created_at', 'updated_at']

class PatientSerializer(serializers.HyperlinkedModelSerializer):
    patientnote_set = PatientNoteSerializer(many=True, read_only=True)

    # We could also have done this in the model:
    # class PatientNote(models.Model):
    #    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    #    # other fields...
    #
    # AND then we could have used this line below instead of the patientnote_set method above:
    # notes = PatientNoteSerializer(many=True, read_only=True)
    #
    # Ref:  https://www.django-rest-framework.org/api-guide/relations/#reverse-relations

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'name', 'date_of_birth', 'age', 'active', 'date_of_last_appointment',
                  'date_of_next_appointment', 'patientnote_set']
        read_only_fields = ['url', 'date_of_last_appointment', 'date_of_next_appointment', 'created_at', 'updated_at']

class AppointmentNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppointmentNote
        fields = ['id', 'appointment', 'text']
        read_only_fields = ['url', 'created_at', 'updated_at']

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    # Forward From the ForeignKey (FFF) (i.e. forward relationship)
    #patient = PatientSerializer(read_only=True)
    #snf = SNFSerializer(read_only=True)
    # Use PrimaryKeyRelatedField for foreign keys, so we can create new appointments with just the ID
    snf = serializers.PrimaryKeyRelatedField(queryset=SNF.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    # Reverse relationship since the ForeignKey is in the AppointmentNote model
    appointmentnote_set = AppointmentNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'title', 'snf', 'date', 'patient', 'appointmentnote_set']
        read_only_fields = ['url', 'created_at', 'updated_at']

    def validate_date(self, value):
        CustomValidators.validate_holiday(value)
        CustomValidators.validate_not_weekend(value)
        return value

    def validate(self, data):
        snf = data.get('snf')
        patient = data.get('patient')
        date = data.get('date')

        if snf and patient and date:
            # Wrapping this in try/catch, to customize the error message to use "date" instead of "non_field_errors"
            try:
                CustomValidators.validate_unique_appointment(snf.id, patient.id, date)
            except ValidationError as e:
                raise ValidationError({'date': str(e.message)})
        return data