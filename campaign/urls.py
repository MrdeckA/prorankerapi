
from django.contrib import admin
from django.urls import path
from campaign.views import CampagneListeView, CampagneDetailView, CandidatListeView, CandidatDetailView, CandidatBulkCreateView, CandidatUpdateCVPathView, CollaborateurListeView, CollaborateurDetailView
from .views import upload_files, file_list


urlpatterns = [
    path('campagnes/', CampagneListeView.as_view(), name='campagne-liste'),
    path('campagnes/<int:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
    path('candidats/', CandidatListeView.as_view(), name='candidat-liste'),
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    path('collaborateurs/', CollaborateurListeView.as_view(),
         name='collaborateur-liste'),
    path('collaborateurs/<int:pk>/',
         CollaborateurDetailView.as_view(), name='collaborateur-detail'),
    path('upload/', upload_files, name='upload_files'),
    path('file-list/', file_list, name='file_list'),
    path('candidats/bulk-create/',
         CandidatBulkCreateView.as_view(), name='candidat-bulk-create'),
    path('candidats/update-cv-path/',
         CandidatUpdateCVPathView.as_view(), name='candidat-update-cv-path'),




]
