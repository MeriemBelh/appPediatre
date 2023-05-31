from django.contrib import admin
from .models import *


class administrateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'nomAdmin', 'prenomAdmin', 'mailAdmin', 'passwordAdmin')
    ordering = ('nomAdmin',)
    search_fields = ('mailAdmin',)


class conversationAdmin(admin.ModelAdmin):
    list_display = ('idConversation', 'sujet', 'receiver', 'sender', 'dateStart', 'dateUpdated', 'nbrMessage')
    ordering = ('idConversation',)
    search_fields = ('idConversation',)


class messageAdmin(admin.ModelAdmin):
    list_display = ('idMessage', 'conversation', 'receiver', 'sender', 'dateEnvoie', 'vu', 'message')
    ordering = ('conversation',)
    search_fields = ('conversation',)


admin.site.register(Administrateur, administrateurAdmin)
admin.site.register(Conversation, conversationAdmin)
admin.site.register(Message, messageAdmin)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Actualite)
