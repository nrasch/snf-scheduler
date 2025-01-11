from django.shortcuts import render
from scheduler.models import SNF
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'main/home.html', context)


@login_required
def snf(request):
    snfs = SNF.objects.all()

    # Handle AJAX request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Create data set to return
        data = list(snfs.values('id', 'name', 'address', 'description', 'phone', 'hour_opens', 'hour_closes', 'max_concurrent_appointments' ))
        return JsonResponse(data, safe=False)
    # If not AJAX, render the template
    else:
        context = {}
        context['snfs'] = snfs
        return render(request, 'main/snf.html', context)


@login_required
@require_http_methods(["POST"])
def delete_snf(request):
    snf_id = request.POST.get('snf_id')
    if not snf_id:
        return JsonResponse({'success': False, 'error': 'SNF ID is required.'}, status=400)

    try:
        # Attempt to fetch the SNF object
        snf = SNF.objects.get(id=snf_id)
        # Delete the SNF object
        snf.delete()
        return JsonResponse({'success': True})
    except SNF.DoesNotExist:
        # If the SNF with the given ID does not exist
        return JsonResponse({'success': False, 'error': 'SNF not found.'}, status=404)
    except Exception as e:
        # Catch any other exceptions, like database errors
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def add_snf(request):
    if request.method == 'POST':
        snf_data = {
            'name': request.POST.get('snf_name'),
            'address': request.POST.get('snf_address'),
            #'phone': request.POST.get('snf_phone'),
            #'email': request.POST.get('snf_email'),
            #'manager': request.POST.get('snf_manager')
        }

        try:
            snf = SNF(**snf_data)
            snf.save()
            return JsonResponse({'success': True})
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
    else:
        try:
            snfs = SNF.objects.all()
            data = list(snfs.values('id', 'name', 'address', 'phone', 'hour_opens', 'hour_closes', 'max_concurrent_appointments'))
            # Convert TimeField to string for JSON serialization
            for snf in data:
                snf['hour_opens'] = str(snf['hour_opens'])
                snf['hour_closes'] = str(snf['hour_closes'])
            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)