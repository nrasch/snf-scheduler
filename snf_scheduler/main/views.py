from django.shortcuts import render
from scheduler.models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
import urllib.parse


# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'main/home.html', context)

#################
### SNF Views ###
#################
@login_required
@require_http_methods(["GET"])
def list_snfs(request):
    snfs = SNF.objects.all()

    # Handle AJAX request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            # Create data set to return
            data = list(snfs.values('id', 'name', 'address', 'description', 'phone', 'hour_opens', 'hour_closes', 'max_concurrent_appointments' ))

            for snf in data:
                snf['hour_opens'] = str(snf['hour_opens'])
                snf['hour_closes'] = str(snf['hour_closes'])

            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    # If not AJAX, render the template
    else:
        context = {}
        context['snfs'] = snfs
        return render(request, 'main/snf.html', context)


@login_required
@require_http_methods(["DELETE"])
def delete_snf(request):
    if request.method == 'DELETE':
        # Since we are sending data in the body of a DELETE request, we will
        # use request.body to get the data instead of request.DELETE
        data = json.loads(request.body)
        snf_id = data.get('snf_id')

        if not snf_id:
            return JsonResponse({'success': False, 'error': 'SNF ID is required.'}, status=400)

        try:
            snf = SNF.objects.get(id=snf_id)
            snf.delete()
            return JsonResponse({'success': True})
        except SNF.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'SNF not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def add_snf(request):
    if request.method == 'POST':
        snf_data = {
            'name': request.POST.get('name'),
            'address': request.POST.get('address'),
            'phone': request.POST.get('phone', '000-000-0000'),  # Default value if not provided
            'hour_opens': request.POST.get('hour_opens', '08:00'),  # Default opening time
            'hour_closes': request.POST.get('hour_closes', '17:00'),  # Default closing time
            'max_concurrent_appointments': int(request.POST.get('max_concurrent_appointments', 0))  # Default to 0
        }

        try:
            # Convert string times to time objects
            snf_data['hour_opens'] = timezone.datetime.strptime(snf_data['hour_opens'], '%H:%M').time()
            snf_data['hour_closes'] = timezone.datetime.strptime(snf_data['hour_closes'], '%H:%M').time()

            snf = SNF(**snf_data)
            snf.save()
            return JsonResponse({'success': True})
        except ValueError as ve:
            # Handle if the time format is incorrect
            return JsonResponse({'success': False, 'error': f'Invalid time format: {str(ve)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
@require_http_methods(["GET"])
def get_snf(request):
    if request.GET.get('snf_id'):
        snf_id = request.GET.get('snf_id')
        try:
            snf = SNF.objects.get(id=snf_id)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': snf.id,
                    'name': snf.name,
                    'address': snf.address,
                    'phone': snf.phone,
                    'hour_opens': str(snf.hour_opens),  # Convert time to string
                    'hour_closes': str(snf.hour_closes),  # Convert time to string
                    'max_concurrent_appointments': snf.max_concurrent_appointments
                }
            })
        except SNF.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'SNF not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["PUT"])
def edit_snf(request):
    # Parse the URL-encoded data
    data = urllib.parse.parse_qs(request.body.decode('utf-8'))

    # Clean and convert data
    snf_data = {}
    for key, value in data.items():
        cleaned_value = value[0].strip().strip('"')

        if key == "max_concurrent_appointments":
            try:
                snf_data[key] = int(cleaned_value)
            except ValueError:
                return JsonResponse({'success': False, 'error': f'Invalid value for {key}: {cleaned_value}'},
                                    status=400)
        elif key in ['hour_opens', 'hour_closes']:
            try:
                snf_data[key] = timezone.datetime.strptime(cleaned_value, '%H:%M:%S').time()
            except ValueError:
                return JsonResponse({'success': False, 'error': f'Invalid time format for {key}: {cleaned_value}'},
                                    status=400)
        else:
            snf_data[key] = cleaned_value

    snf_id = snf_data.get('snf_id')
    if not snf_id:
        return JsonResponse({'success': False, 'error': 'SNF ID is required.'}, status=400)

    try:
        # Retrieve the SNF object
        snf = SNF.objects.get(id=snf_id)

        # Update the SNF object
        for key, value in snf_data.items():
            if hasattr(snf, key):
                setattr(snf, key, value)

        # Save changes
        snf.save()
        return JsonResponse({'success': True, 'message': 'SNF updated successfully.'})

    except SNF.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'SNF not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


#####################
### Patient Views ###
#####################
@login_required
@require_http_methods(["GET"])
def list_patients(request):
    patients = Patient.objects.all()

    # Handle AJAX request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            data = []
            # We are looping through the patients and creating a dictionary for each patient, because
            # we cannot directly serialize the queryset to JSON using list(patients.values()) or patients.values()
            # This due to the Patient model having two computed fields:  `age` and `name`
            # Properties defined on the model are not included by default.
            for patient in patients:
                data.append({
                    'id': patient.id,
                    'name': patient.name, # Directly using the name property from the model
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'date_of_birth': patient.date_of_birth,
                    'age': patient.age,  # Directly using the age property from the model
                    'date_of_last_appointment': patient.date_of_last_appointment,
                    'date_of_next_appointment': patient.date_of_next_appointment,
                    'active': patient.active
                })

            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    # If not AJAX, render the template
    else:
        context = {'patients': patients}
        return render(request, 'main/patient.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_patient(request):
    if request.method == 'DELETE':
        # Since we are sending data in the body of a DELETE request, we will
        # use request.body to get the data instead of request.POST
        data = json.loads(request.body)
        patient_id = data.get('patient_id')

        if not patient_id:
            return JsonResponse({'success': False, 'error': '{Patient} ID is required.'}, status=400)

        try:
            patient = Patient.objects.get(id=patient_id)
            patient.delete()
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def add_patient(request):
    if request.method == 'POST':
        patient_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'active': request.POST.get('active', False)
        }

        try:
            patient = Patient(**patient_data)
            patient.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
@require_http_methods(["GET"])
def get_patient(request):
    if request.GET.get('patient_id'):
        patient_id = request.GET.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': patient.id,
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'date_of_birth': patient.date_of_birth,
                    'active': patient.active
                }
            })
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["PUT"])
def edit_patient(request):
    # Parse the URL-encoded data
    data = urllib.parse.parse_qs(request.body.decode('utf-8'))

    # Clean and convert data
    patient_data = {}
    for key, value in data.items():
        patient_data[key] = value[0].strip().strip('"')

    if 'active' not in data.keys():
        patient_data['active'] = False
    else:
        patient_data['active'] = True

    patient_id = patient_data.get('patient_id')
    if not patient_id:
        return JsonResponse({'success': False, 'error': 'Patient ID is required.'}, status=400)

    try:
        # Retrieve the Patient object
        patient = Patient.objects.get(id=patient_id)

        # Update the Patient object
        for key, value in patient_data.items():
            if hasattr(patient, key):
                setattr(patient, key, value)

        # Save changes
        patient.save()
        return JsonResponse({'success': True, 'message': 'Patient updated successfully.'})

    except Patient.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)