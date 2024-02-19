
from django.contrib import admin
from django.urls import path
from campaign.views import CampagneListeView, CampagneDetailView, CandidatListeView, CandidatDetailView, CollaborateurListeView, CollaborateurDetailView, lire_contenu_pdf, charger_contenu_pdfs


urlpatterns = [
    path('campagnes/', CampagneListeView.as_view(), name='campagne-liste'),
    path('campagnes/<int:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
    path('candidats/', CandidatListeView.as_view(), name='candidat-liste'),
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    path('collaborateurs/', CollaborateurListeView.as_view(),
         name='collaborateur-liste'),
    path('collaborateurs/<int:pk>/',
         CollaborateurDetailView.as_view(), name='collaborateur-detail'),
    #     path('prediction/start/',
    #          CollaborateurDetailView.as_view(), name='start-prediction'),
    path('prediction/start/', lire_contenu_pdf, name='start-prediction'),
    path('charger_contenu_pdfs/', charger_contenu_pdfs,
         name='charger_contenu_pdfs'),
]
