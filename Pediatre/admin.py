from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class PediatreAdmin(admin.ModelAdmin):
    list_display = ('inpe', 'nomPediatre', 'prenomPediatre', 'mailPediatre', 'passwordPediatre')
    ordering = ('inpe',)
    search_fields = ('nomPediatre',)

admin.site.register(Pediatre, PediatreAdmin)
admin.site.register(User)
