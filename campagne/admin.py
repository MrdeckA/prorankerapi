from django.contrib import admin

# Register your models here.
from .models import Campagne


class UserAdmin(admin.ModelAdmin):
    list_display = ('nom', 'intitule_poste', 'user')




admin.site.register(Campagne, UserAdmin)

