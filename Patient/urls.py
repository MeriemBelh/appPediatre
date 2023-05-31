from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.password_validation import MinimumLengthValidator

urlpatterns = [
    path('home_patient/', views.home_patient, name="home_patient"),
    path('profile/', views.profile, name="profile"),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password.as_view(template_name="Patient/password.html"),
        name="update_password"),
    path('consultation_dossier/', views.infos_patient, name='info_patient'),
    path('imprimer_dossier_patient_pdf/', views.imprimer_dossier_patient_pdf, name='imprimer_dossier_patient_pdf'),
    path('password_success/', views.password_success, name="password_success"),
    path('logout_patient', views.logout_patient, name='logout_patient'),
]
