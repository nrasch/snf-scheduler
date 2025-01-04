from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import SNF, Patient, Appointment, AppointmentNote, PatientNote
from .serializers import SNFSerializer, PatientSerializer, AppointmentSerializer, AppointmentNoteSerializer, PatientNoteSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from authentication.mixins import EditorControlMixin


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snfs': reverse('snf-list-create', request=request, format=format),
        'patients': reverse('patient-list-create', request=request, format=format),
        'appointments': reverse('appointment-list-create', request=request, format=format),
        'appointment-notes': reverse('appointment-notes-list-create', request=request, format=format),
        'patient-notes': reverse('patient-notes-list-create', request=request, format=format),
    })

class SNFListCreate(EditorControlMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer

class SNFDetail(EditorControlMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = SNF.objects.all()
    serializer_class = SNFSerializer

class PatientListCreate(EditorControlMixin, generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetail(EditorControlMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentListCreate(EditorControlMixin, generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(EditorControlMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentNoteListCreate(EditorControlMixin, generics.ListCreateAPIView):
    queryset = AppointmentNote.objects.all()
    serializer_class = AppointmentNoteSerializer

class AppointmentNoteDetail(EditorControlMixin, generics.RetrieveUpdateDestroyAPIView):  # Change here
    queryset = AppointmentNote.objects.all()
    serializer_class = AppointmentNoteSerializer

class PatientNoteListCreate(EditorControlMixin, generics.ListCreateAPIView):
    queryset = PatientNote.objects.all()
    serializer_class = PatientNoteSerializer

class PatientNoteDetail(EditorControlMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientNote.objects.all()
    serializer_class = PatientNoteSerializer