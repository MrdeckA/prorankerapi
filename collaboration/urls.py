from django.urls import path

from .views import CollaborationListeView, CollaborationDetailView

urlpatterns = [
    path('', CollaborationListeView.as_view(), name='collaboration-liste'),
    path('<int:pk>/', CollaborationDetailView.as_view(), name='collaboration-detail'),
]