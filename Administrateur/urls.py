from django.urls import path, include
from . import views

urlpatterns = [
    # gestion session
    path('', views.index_admin, name="index_admin"),
    path('nouveau-administrateur/', views.new_admin, name='new_admin'),
    path('logout-administrateur/', views.logout_admin, name='logout_admin'),
    # path('login_administrateur/', views.connexion_administrateur, name='connexion_administrateur'),

    # Gestion admin
    path('gestion_administrateurs/', views.gestion_administrateurs, name='gestion_administrateurs'),
    path('ajouter_administrateur/', views.ajouter_administrateur, name='ajouter_administrateur'),
    path('recherche_administrateur/', views.recherche_administrateur, name='recherche_administrateur'),
    path('afficher_administrateur/<str:admin>/', views.afficher_administrateur, name='afficher_administrateur'),
    path('editer_admin/<str:admin>/', views.editer_admin, name='editer_admin'),
    path('supprimer_admin/<str:admin>/', views.supprimer_admin, name='supprimer_admin'),
    path('desactiver_admin/<str:admin>/', views.desactiver_admin, name='desactiver_admin'),
    path('activer_admin/<str:admin>/', views.activer_admin, name='activer_admin'),

    # Messagerie
    path('chatAdmin/', views.chatAdmin, name='chatAdmin'),
    path('conversation_admin/<int:conversation_id>/', views.conversation_admin, name='conversation_admin'),

    # gestion patients
    path('gestion_patients/', views.gestion_patients, name='gestion_patients'),
    path('ajouter_patient/', views.ajouter_patient, name='ajouter_patient_admin'),
    path('recherche_patient/', views.recherche_patient, name='recherche_patient_admin'),
    path('editer_patient/<int:patient_id>/', views.editer_patient, name='editer_patient'),
    path('supprimer_patient/<int:patient_id>/', views.supprimer_patient, name='supprimer_patient'),
    path('desactiver_patient/<int:patient_id>/', views.desactiver_patient, name='desactiver_patient'),
    path('activer_patient/<int:patient_id>/', views.activer_patient, name='activer_patient'),
    path('afficher_patient/<int:patient_id>/', views.afficher_patient, name='afficher_patient'),
    path('line_chart_Obesite/<int:patient_id>/', views.line_chart_Obesite, name='line_chart_Obesite'),

    path('delegationCities_ajax/', views.delegationCities_ajax, name='delegationCities_ajax'),

    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),
    path('pie_chart_sexe/', views.pie_chart_sexe, name='pie_chart_sexe'),
    path('pie_chart_region/', views.pie_chart_region, name='pie_chart_region'),
    path('pie_chart_cm/', views.pie_chart_cm, name='pie_chart_cm'),
    path('pie_chart_ville/', views.pie_chart_ville, name='pie_chart_ville'),
    path('pie_chart_pc/', views.pie_chart_pc, name='pie_chart_pc'),
    path('pie_chart_gs/', views.pie_chart_gs, name='pie_chart_gs'),
    path('pie_chart_tg/', views.pie_chart_tg, name='pie_chart_tg'),
    path('pie_chart_av/', views.pie_chart_av, name='pie_chart_av'),
    path('pie_chart_sn/', views.pie_chart_sn, name='pie_chart_sn'),
    path('pie_chart_pn/', views.pie_chart_pn, name='pie_chart_pn'),
    path('pie_chart_han/', views.pie_chart_han, name='pie_chart_han'),
    path('pie_chart_allaitement/', views.pie_chart_allaitement, name='pie_chart_allaitement'),
    path('pie_chart_rsp/', views.pie_chart_rsp, name='pie_chart_rsp'),

    # gestion media
    path('affichage_image/', views.afficherImg, name='affichage_image'),
    path('ajout_image/', views.ajouterImg, name='ajout_image'),
    path('modifier_image/<int:image_id>/', views.modifierImg, name='modifier_image'),
    path('supprimer_image/<int:image_id>/', views.supprimerImage, name='supprimer_image'),
    path('affichage_video/', views.afficherVideo, name='affichage_video'),
    path('ajout_video/', views.ajouterVideo, name='ajout_video'),
    path('modifier_video/<int:video_id>/', views.modifierVideo, name='modifier_video'),
    path('supprimer_video/<int:video_id>/', views.supprimerVideo, name='supprimer_video'),

    # gestion news

    path('affichage_actualite/', views.afficherActualite, name='affichage_actualite'),
    path('ajout_actualite/', views.ajouterActualite, name='ajout_actualite'),
    path('supprimer_actualite/<int:actualite_id>/', views.supprimerActualite, name='supprimer_actualite'),
    path('modifer_actualite/<int:actualite_id>/', views.modifierActualite, name='modifer_actualite'),

]
