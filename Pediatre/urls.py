from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.pediatre, name='pediatre'),
    path('index_pediatre', views.index_pediatre, name='index_pediatre'),
    path('logout_pediatre', views.logout_pediatre, name='logout_pediatre'),
    path('login_pediatre/', views.login_pediatre, name='login_pediatre'),
    path('nouveau_pediatre/', views.nouveau_pediatre, name='nouveauPediatre'),
    path('home_pediatre/', views.home_pediatre, name='home_pediatre'),
    path('recherche_patient/', views.recherche_patient, name='recherche_patient'),
    path('corbeille_patient/', views.corbeille_patient, name='corbeille_patient'),
    path('messagerie_pediatre/', views.messagerie_pediatre, name='messagerie_pediatre'),
    path('recherche_conversation_pediatre/', views.recherche_conversation_pediatre, name='recherche_conversation_pediatre'),
    path('new_conversation_pediatre/', views.new_conversation_pediatre, name='new_conversation_pediatre'),
    path('home_pediatre/ajouter_patient/', views.ajouter_patient_pediatre, name='ajouter_patient'),

    path('afficher_infos_patient/<int:patient_id>/', views.afficher_infos_patient, name='afficher_infos_patient'),
    path('imprimer_dossier_patient_pdf/<int:patient_id>/', views.imprimer_dossier_patient_pdf, name='imprimer_dossier_patient_pdf'),
    path('supprimer_patient/<int:patient_id>/', views.supprimer_patient, name='supprimer_patient'),
    path('modifier_patient/<int:patient_id>/', views.modifier_patient, name='modifier_patient'),
    path('add_patient_corbeille/<int:patient_id>/', views.add_patient_corbeille, name='add_patient_corbeille'),
    path('restore_patient_corbeille/<int:patient_id>/', views.restore_patient_corbeille, name='restore_patient_corbeille'),
    path('conversation_pediatre/<int:conversation_id>/', views.conversation_pediatre, name='conversation_pediatre'),
    path('send_message_pediatre/<int:conversation_id>/', views.send_message_pediatre, name='send_message_pediatre'),

    path('delegationCities_ajax/', views.delegationCities_ajax, name='delegationCities_ajax'),
    path('classes_ajax/', views.classes_ajax, name='classes_ajax'),
    path('conversation_pediatre_ajax/<int:conversation_id>/', views.conversation_pediatre_ajax, name='conversation_pediatre_ajax'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
