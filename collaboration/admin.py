from django.contrib import admin
from .models import Collaboration
# Register your models here.

from .models import Collaboration
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('inviteur', 'invite', 'role', 'statut_invitation')




admin.site.register(Collaboration, CollaborationAdmin)

