from django_filters import rest_framework as filters
import django_filters
from .models import Campagne, Candidat, Collaborateur


class CampagneFilter(django_filters.FilterSet):
    class Meta:
        model = Campagne
        fields = '__all__'


# to do
class CandidatFilter(django_filters.FilterSet):
    campagne__id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Candidat
        fields = '__all__'


class CollaborateurFilter(django_filters.FilterSet):
    user__id = filters.CharFilter(lookup_expr='icontains')
    campagne__id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Collaborateur
        fields = '__all__'
