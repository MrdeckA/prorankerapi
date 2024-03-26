
from django_filters import rest_framework as filters
import django_filters
from .models import Candidat
from collaboration.models import Collaboration
from django.db import models

class CandidatFilter(django_filters.FilterSet):
    campagne__id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Candidat
        fields = '__all__'