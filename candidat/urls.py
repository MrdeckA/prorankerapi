from django.urls import path

from .views import CandidatDetailView, CandidatListeView

urlpatterns = [
    path('', CandidatListeView.as_view(), name='candidat-liste'),
    path('<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
]