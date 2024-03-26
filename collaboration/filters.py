from django_filters import rest_framework as filters
import django_filters
from candidat.models import Candidat

class CollaborationFilter(django_filters.FilterSet):
    campagne__id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Candidat
        fields = '__all__'