from django.shortcuts import render
from scheduler.models import SNF
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json


# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'main/home.html', context)


@login_required
@require_http_methods(["GET"])
def list_snf(request):
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
        # use request.body to get the data instead of request.POST
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
            'name': request.POST.get('snf_name'),
            'address': request.POST.get('snf_address'),
            'phone': request.POST.get('snf_phone', '000-000-0000'),  # Default value if not provided
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