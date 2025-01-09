from django.shortcuts import render
from scheduler.models import SNF
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
def home(request):
    context = {}
    return render(request, 'main/home.html', context)

def snf(request):
    snfs = SNF.objects.all()

    # Handle AJAX request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Create data set to return
        data = list(snfs.values('id', 'name', 'address'))
        return JsonResponse(data, safe=False)
    # If not AJAX, render the template
    else:
        context = {}
        context['snfs'] = snfs
        return render(request, 'main/snf.html', context)


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

