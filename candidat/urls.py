from django.urls import path

from .views import CandidatDetailView, CandidatListeView, CandidatDetail

urlpatterns = [
    path('', CandidatListeView.as_view(), name='candidat-liste'),
    path('<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    path('by-user/', CandidatDetail.as_view(), name='candidat-user'),
]