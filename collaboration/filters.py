from django_filters import rest_framework as filters
import django_filters
from .models import Collaboration

class CollaborationFilter(django_filters.FilterSet):
    campagne__id = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Collaboration
        fields = '__all__'