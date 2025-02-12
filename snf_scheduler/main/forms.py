from django import forms
from scheduler.models import SNF, Patient, Appointment, AppointmentNote, PatientNote

class SNFForm(forms.ModelForm):
    class Meta:
        model = SNF
        fields = ['id', 'name', 'description', 'address', 'phone', 'hour_opens', 'hour_closes', 'max_concurrent_appointments']
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'autofocus': 'autofocus'}),  # Set focus to this field
            'description': forms.Textarea(attrs={'rows': 3}),  # Adjust rows as needed
            'address': forms.Textarea(attrs={'rows': 2}),
            'hour_opens': forms.TimeInput(attrs={'type': 'time'}),
            'hour_closes': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'name': 'Facility Name',  # More descriptive label
            'max_concurrent_appointments': 'Max Appointments',  # More concise label
        }
        help_texts = {
            'phone': 'Enter phone number in format XXX-XXX-XXXX',
            'hour_opens': '12 hour format',
            'hour_closes': '12 hour format',
        }
        error_messages = {
            'name': {
                'required': "Facility Name is required.",
            },
            'address': {
                'required': "Address is required.",
            },
            'phone': {
                'required': "Phone number is required.",
                'invalid': "Enter a valid phone number.",
            },
            'hour_opens': {
                'required': "Opening hour is required.",
                'invalid': "Enter a valid time for the opening hour.",
            },
            'hour_closes': {
                'required': "Closing hour is required.",
                'invalid': "Enter a valid time for the closing hour.",
            },
            'max_concurrent_appointments': {
                'invalid': "Please enter a valid number",
                'required': "Max Appointments is required",
            },
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Basic phone number validation (you can use a more robust regex)
        if phone and len(phone) != 12 or not all(c.isdigit() or c == '-' for c in phone) or phone[3] != '-' or phone[7] != '-':
            raise forms.ValidationError("Invalid phone number format. Use XXX-XXX-XXXX")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        hour_opens = cleaned_data.get('hour_opens')
        hour_closes = cleaned_data.get('hour_closes')

        if hour_opens and hour_closes and hour_opens >= hour_closes:
            raise forms.ValidationError("Opening time must be before closing time.")

        return cleaned_data


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'active']
        widgets = {
            'id': forms.HiddenInput(),
            'first_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),  # Set focus to this field
            'last_name': forms.TextInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'active': forms.CheckboxInput(),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        help_texts = {
            'phone': 'Enter phone number in format XXX-XXX-XXXX',
            'date_of_birth': 'Date of birth',
        }
        error_messages = {
            'first_name': {
                'required': "First Name is required.",
            },
            'last_name': {
                'required': "Last Name is required.",
            },
            'date_of_birth': {
                'required': "Date of birth is required.",
                'invalid': "Enter a valid date.",
            }
        }