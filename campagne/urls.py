from django.urls import path

from .views import CampagneDetailView, CampagneListeView, CampagneRankingView, CampagneAddFileView

urlpatterns = [
    path('', CampagneListeView.as_view(), name='campagne-liste'),
    path('<int:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
    path('add-file/<int:pk>/', CampagneAddFileView.as_view(), name='campagne-add-file'),
    path('start/ranking', CampagneRankingView.as_view(), name='start-prediction'),
]