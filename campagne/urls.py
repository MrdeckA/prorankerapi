from django.urls import path

from .views import CampagneDetailView, CampagneListeView

urlpatterns = [
    path('', CampagneListeView.as_view(), name='campagne-liste'),
    path('<str:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
]