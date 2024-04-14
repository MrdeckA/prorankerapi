from django.shortcuts import render
from .models import Candidat
from .serializer import CandidatSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics, status
from .filters import CandidatFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class CandidatListeView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter
    permission_classes = [IsAuthenticated]


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated]
    


class CandidatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter
    
    
    
    def get(self, request, *args, **kwargs):
        
        
        
        try:
            user_id = request.GET.get('user')

            if user_id is None:
                return Response({"message": "Paramètre 'user' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            paginator = PageNumberPagination()
            resultats_page = paginator.paginate_queryset(self.queryset, request)
            
            candidats_utilisateur = Candidat.objects.filter(campagne__user_id=user_id)
            
            
            final = paginator.get_paginated_response(CandidatSerializer(candidats_utilisateur, many=True).data).data
            return Response( final, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


