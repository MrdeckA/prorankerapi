from django.contrib import admin

# Register your models here.
from .models import Candidat
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'campagne')




admin.site.register(Candidat, CandidatAdmin)

