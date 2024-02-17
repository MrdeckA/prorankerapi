
from django.contrib import admin
from django.urls import path
from campaign.views import CampagneListeView, CampagneDetailView, CandidatListeView, CandidatDetailView, CollaborateurListeView, CollaborateurDetailView


urlpatterns = [
    path('campagnes/', CampagneListeView.as_view(), name='campagne-liste'),
    path('campagnes/<int:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
    path('candidats/', CandidatListeView.as_view(), name='candidat-liste'),
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    path('collaborateurs/', CollaborateurListeView.as_view(),
         name='collaborateur-liste'),
    path('collaborateurs/<int:pk>/',
         CollaborateurDetailView.as_view(), name='collaborateur-detail'),





]
