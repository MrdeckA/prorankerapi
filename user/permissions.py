from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from user.models import User

class ManagePermission(BasePermission):
    def has_permission(self, request, view):
        
        id = request.parser_context['kwargs']['id']
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'detail':'Utilisateur non identifié.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(({'detail':'Identifiant invalide.'}), status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_admin and not request.user == user:
            raise PermissionDenied(detail='Accès refusé.')
        
        return super().has_permission(request, view)
    
class AllUserPermission(BasePermission):
    def has_permission(self, request, view):
        
        if not request.user.is_admin:
            raise PermissionDenied(detail='Accès refusé.')
        
        return super().has_permission(request, view)