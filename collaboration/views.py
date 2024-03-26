from django.shortcuts import render
from rest_framework import generics
from .models import Collaboration
from .filters import CollaborationFilter
from .serializer import CollaborationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class CollaborationListeView(generics.ListCreateAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborationFilter
    permission_classes = [IsAuthenticated]



class CollaborationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    permission_classes = [IsAuthenticated]