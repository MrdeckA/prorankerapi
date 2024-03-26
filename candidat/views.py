from django.shortcuts import render
from .models import Candidat
from .serializer import CandidatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, status
from .filters import CandidatFilter

# Create your views here.
class CandidatListeView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
