from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from .serializers import SNFSerializer
from rest_framework import generics

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snfs': reverse('snf-list-create', request=request, format=format),
    })

class SNFListCreate(generics.ListCreateAPIView):
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer

class SNFDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer
