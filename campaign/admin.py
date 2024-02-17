from django.contrib import admin
from .models import Campagne, Candidat, Collaborateur, Langue, Competence


class CampagneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'intitule_poste')


class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'campagne', 'cv_path', 'adresse',
                    'email', 'telephone', 'cv_data_url', 'cv_original_name')


class CollaborateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'campagne')


class LangueAdmin(admin.ModelAdmin):
    list_display = ('nom')


class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom')


admin.site.register(Campagne, CampagneAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Collaborateur, CollaborateurAdmin)
admin.site.register(Langue)
admin.site.register(Competence)
