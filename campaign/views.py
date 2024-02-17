from django.shortcuts import render
from .apps import CampaignConfig
# Create your views here.
# views.py
import sys
import fitz
from rest_framework import generics
from .models import Campagne, Candidat, Collaborateur
from .serializers import CampagneSerializer, CandidatSerializer, CollaborateurSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import base64
import requests
import os
from django.views import View
from django.utils.decorators import method_decorator
import json
from rest_framework.decorators import api_view

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from django_filters import rest_framework as filters
from .filters import CollaborateurFilter, CampagneFilter, CandidatFilter


class CampagneListeView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter


class CampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer


class CandidatListeView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer


class CollaborateurListeView(generics.ListCreateAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborateurFilter


class CollaborateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer
