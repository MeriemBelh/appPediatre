from django.contrib import admin
from .models import *

class PatientAdmin(admin.ModelAdmin):
    list_display = ('inpe', 'idPatient','nomPatient', 'prenomPatient', 'dateNaissancePatient', 'mailPatient','is_deleted')
    ordering = ('idPatient',)
    search_fields = ('nomPatient',)


class PatientActiviteAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'type_activite', 'description_activite')
    ordering = ('patientID',)
    search_fields = ('patientID',)

class PatientScolariteAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'type_scolarite', 'level_scolarite', 'year_scolarite')
    ordering = ('patientID',)
    search_fields = ('patientID',)

class PathologieCardiqueOpereAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'opere_date', 'opere_type')
    ordering = ('patientID',)
    search_fields = ('patientID',)

class GenerateIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'idPatient')
    ordering = ('idPatient',)
    search_fields = ('idPatient',)

class InfoPatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'scolarise','activite_sportive','activite_artistique','activite_prof')
    ordering = ('patient',)
    search_fields = ('patient',)

class DelegationAdmin(admin.ModelAdmin):
    list_display = ('idDelegation', 'nomDelegation')
    ordering = ('idDelegation',)
    search_fields = ('nomDelegation',)

class VilleAdmin(admin.ModelAdmin):
    list_display = ('idVille', 'delegation', 'nomVille')
    ordering = ('idVille',)
    search_fields = ('nomVille',)

class ClassePrimaireAdmin(admin.ModelAdmin):
    list_display = ('idClassePrimaire', 'classePName')
    ordering = ('idClassePrimaire',)
    search_fields = ('idClassePrimaire',)

class ClasseSecondaireAdmin(admin.ModelAdmin):
    list_display = ('idClasseSecondaire', 'classeSName')
    ordering = ('idClasseSecondaire',)
    search_fields = ('idClasseSecondaire',)

class MutuelleAdmin(admin.ModelAdmin):
    list_display = ('idMutuelle', 'mutuelleName')
    ordering = ('idMutuelle',)
    search_fields = ('mutuelleName',)

class ObesiteImcAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'obesite_date', 'obesite_poids', 'obesite_taille', 'imc')
    ordering = ('patientID',)
    search_fields = ('patientID',)

class CorbeillePatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'dateSuppression_debut', 'dateSuppression_fin')
    ordering = ('patient',)
    search_fields = ('patient',)

class PathologieDentaireAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'date_act', 'dent_GaucheDroit','dent_HautBas', 'dent_num', 'code_act')
    ordering = ('patientID',)
    search_fields = ('patientID',)

admin.site.register(Patient, PatientAdmin)
admin.site.register(PathologieCardiqueOpere, PathologieCardiqueOpereAdmin)
admin.site.register(PatientActivite, PatientActiviteAdmin)
admin.site.register(PatientScolarite, PatientScolariteAdmin)
admin.site.register(InfoPatient, InfoPatientAdmin)
admin.site.register(GenerateID, GenerateIDAdmin)
admin.site.register(Delegation, DelegationAdmin)
admin.site.register(Ville, VilleAdmin)
admin.site.register(ClasseSecondaire, ClasseSecondaireAdmin)
admin.site.register(ClassePrimaire, ClassePrimaireAdmin)
admin.site.register(Mutuelle, MutuelleAdmin)
admin.site.register(ObesiteImc, ObesiteImcAdmin)
admin.site.register(CorbeillePatient, CorbeillePatientAdmin)
admin.site.register(PathologieDentaire, PathologieDentaireAdmin)