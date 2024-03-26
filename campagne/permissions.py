from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
    

    
class AllPermission(BasePermission):
    def has_permission(self, request, view):
        
        
        return super().has_permission(request, view)