from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from .serializers import SNFSerializer, PatientSerializer, AppointmentSerializer, AppointmentNoteSerializer, PatientNoteSerializer
from rest_framework import generics
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snfs': reverse('snf-list-create', request=request, format=format),
        'patients': reverse('patient-list-create', request=request, format=format),
        'appointments': reverse('appointment-list-create', request=request, format=format),
        'appointment-notes': reverse('appointment-notes-list-create', request=request, format=format),
        'patient-notes': reverse('patient-notes-list-create', request=request, format=format),
    })

class SNFListCreate(generics.ListCreateAPIView):
    #authentication_classes = [TokenAuthentication]  # If not set as default in settings
    permission_classes = [IsAuthenticated]
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer

class SNFDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer

class PatientListCreate(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentListCreate(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentNoteListCreate(generics.ListCreateAPIView):
    queryset = AppointmentNote.objects.all()
    serializer_class = AppointmentNoteSerializer

class AppointmentNoteDetail(generics.RetrieveUpdateDestroyAPIView):  # Change here
    queryset = AppointmentNote.objects.all()
    serializer_class = AppointmentNoteSerializer

class PatientNoteListCreate(generics.ListCreateAPIView):
    queryset = PatientNote.objects.all()
    serializer_class = PatientNoteSerializer

class PatientNoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientNote.objects.all()
    serializer_class = PatientNoteSerializer