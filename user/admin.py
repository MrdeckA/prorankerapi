from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'email_valid', 'nom_complet')




admin.site.register(User, UserAdmin)

