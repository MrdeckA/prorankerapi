from django_filters import rest_framework as filters
import django_filters
from .models import Campagne
from candidat.models import Candidat
from collaboration.models import Collaboration
from django.db import models


class CampagneFilter(django_filters.FilterSet):
    class Meta:
        model = Campagne
        fields = '__all__'
        filter_overrides = {
            models.JSONField: {
                'filter_class': django_filters.CharFilter,
            },
        }
