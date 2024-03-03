from django.contrib import admin
from .models import Campagne, Candidat, Collaboration


class CampagneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description_poste', 'intitule_poste')


class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'campagne', 'cv_path', 'adresse',
                    'email', 'telephone', 'cv_data_url', 'cv_original_name')


class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('inviteur', 'invite')


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom')


admin.site.register(Campagne, CampagneAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Collaboration, CollaborationAdmin)
