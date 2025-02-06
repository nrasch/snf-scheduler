from django.shortcuts import render
from scheduler.models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SNFForm, PatientForm


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
def add_snf(request):
    if request.method == 'GET':
        form = SNFForm()
        return render(request, 'main/add_snf.html', {'form': form})

    if request.method == 'POST':
        form = SNFForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render(request, 'main/add_snf.html', {'form': form})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def edit_snf(request, pk):
    if request.method == 'GET':
        snf = SNF.objects.get(pk=pk)
        form = SNFForm(instance=snf)
        return render(request, 'main/edit_snf.html', {'form': form})

    if request.method == 'POST':
        snf = SNF.objects.get(pk=pk)
        form = SNFForm(request.POST, instance=snf)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render(request, 'main/edit_snf.html', {'form': form})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


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
def add_patient(request):
    if request.method == 'GET':
        form = PatientForm()
        return render(request, 'main/add_patient.html', {'form': form})

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Patient added successfully.'})
        else:
            print("Inside add_patient::POST::is_valid::else")
            print(form.errors)
        return render(request, 'main/add_patient.html', {'form': form})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def delete_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_id = data.get('patient_id')

        if not patient_id:
            return JsonResponse({'success': False, 'error': '{Patient} ID is required.'}, status=400)

        try:
            patient = Patient.objects.get(id=patient_id)
            message = f'Patient {patient.name} (ID: {patient_id}) deleted successfully.'
            patient.delete()
            return JsonResponse({'success': True, 'message': message})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


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
def edit_patient(request, pk):
    if request.method == 'GET':
        patient = Patient.objects.get(pk=pk)
        form = PatientForm(instance=patient)
        form.id = patient.id
        return render(request, 'main/edit_patient.html', {'form': form, 'patient': patient})

    if request.method == 'POST':
        patient = Patient.objects.get(pk=pk)
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render(request, 'main/edit_patient.html', {'form': form})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)