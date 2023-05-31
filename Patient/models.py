from django.db import models, transaction
from Pediatre.models import *

from datetime import datetime, timedelta
from django.utils import timezone

OUINON = (
    ("1", "Non"),
    ("2", "Oui"),
)
TermeGrossesse = (
    ("1", "A terme"),
    ("2", "Prématuré"),
)
TYPEACCOUCHEMENT = (
    ("1", "Basse"),
    ("2", "Césarienne"),
)
POIDSNAISSANCE = (
    ("1", "< 2Kg"),
    ("2", "2--2,5Kg"),
    ("3", "2,5--4Kg"),
    ("4", "> 4Kg"),
)
ALLAITEMENT = (
    ("1", "Maternel"),
    ("2", "Mixte"),
    ("3", "Artificiel"),
)
RETENTISSEMENT = (
    ("1", "Retard"),
    ("2", "Stagnation"),
    ("3", "Bon"),
)
POTENTIELAUDITIF = (
    ("1", "Normaux"),
    ("2", "Surdité totale"),
    ("3", "Surdité partielle"),
)
CARYOTYPE = (
    ('NonFait', "Non fait"),
    ('Fait', (
        ('1', 'Libre et homogène'),
        ('2', 'Mosaique'),
        ('3', 'Partielle'),
        ('4', 'Translocation'),
    ))
)
PATHOLOGIEENDOCRINIENNE = (
    ("1", "Hypothyroïdie"),
    ("2", "Euthyroïdie"),
)
ECHOCOEUR = (
    ("1", "Normal"),
    ("2", "Cardiopathie congénitale"),
)
HERNIS= (
    ("1", "Aucune"),
    ("2", "Ombilical"),
    ("3", "Inguinale"),
)
TROUBLEDIGESTIF= (
    ("1", "Constipation"),
    ("2", "Diarrhée"),
    ("3", "Normal"),
)
def default_image():
    return 'Uploads/imgProfile_patient/default-user-image.png'

def get_and_update_generate_id():
    with transaction.atomic():
        generate_id = GenerateID.objects.select_for_update().first()
        if not generate_id:
            # Initialize GenerateID with a value of 1
            GenerateID.objects.create(idPatient=14573)
            return 1
        else:
            new_value = generate_id.idPatient + 1
            generate_id.idPatient = new_value
            generate_id.save()
            return new_value

def get_default_datetime():
    current_datetime = timezone.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')

def add_30_days():
    current_datetime = datetime.now() + timedelta(days=30)
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')


class GenerateID(models.Model):
    id = models.AutoField(primary_key=True)
    idPatient = models.IntegerField()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    idPatient = models.IntegerField(unique=True, default=get_and_update_generate_id)
    inpe = models.ForeignKey(Pediatre, null=True, on_delete=models.SET_NULL)
    passwordPatient = models.CharField(max_length=100,null=True)
    sexePatient = models.CharField(default="Unisexe",max_length=100,null=True)
    nomPatient = models.CharField(max_length=60,null=True)
    prenomPatient = models.CharField(max_length=60,null=True)
    dateNaissancePatient = models.DateField(null=True)
    mailPatient = models.EmailField(null=True)
    adressePatient = models.TextField(max_length=300,null=True)
    numTelephoneMere = models.IntegerField(null=True)
    numTelephonePere = models.IntegerField(null=True)
    villePatient = models.CharField(max_length=100,null=True)
    delegationPatient = models.CharField(max_length=100,null=True)
    couvertureMedical = models.CharField(max_length=200,null=True)
    nomCouvertureMedical = models.CharField(default="",max_length=200,null=True)
    imgPatient = models.ImageField(upload_to='imgProfile_patient/', blank=True, default=default_image)
    is_deleted = models.CharField(default="Non", max_length=3, null=False)

    def __str__(self):
        return str(self.idPatient) + "-" + str(self.nomPatient) + "." + str(self.prenomPatient)

class CorbeillePatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    dateSuppression_debut = models.DateField(null=False, default=get_default_datetime())
    dateSuppression_fin = models.DateField(null=False, default=add_30_days())

    def __str__(self):
        return str(self.patient)

class InfoPatient(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    parents_Consanguins = models.CharField(max_length=20, default="Non",null=True, blank=True)
    #Age maternel à l'accouchement
    age_maternel_accouchement = models.IntegerField(default=100, null=True, blank=True)
    grossesse_suivi = models.CharField(max_length=100, default="Non",null=True, blank=True)
    terme_grossesse = models.CharField(max_length=200, choices=TermeGrossesse, default='1',null=True, blank=True)
    precisionTerme = models.CharField(max_length=100, default="",null=True, blank=True)
    accouchement_par_voie = models.CharField(max_length=200, choices=TYPEACCOUCHEMENT, default='1',null=True, blank=True)
    souffrance_neonatal = models.CharField(max_length=100, default="Non",null=True, blank=True)
    poids_de_naissance = models.CharField(max_length=100, choices=POIDSNAISSANCE, default='1',null=True, blank=True)
    taille_de_naissance = models.CharField(max_length=100, default="",null=True, blank=True)
    Notion_hospitalisation_age_neonatal = models.CharField(max_length=100,default="Non",null=True, blank=True)
    allaitement = models.CharField(max_length=100, choices=ALLAITEMENT, default='1',null=True, blank=True)
    diversification_alimentaire = models.CharField(max_length=100, default="",null=True, blank=True)
    retentissement_staturo_ponderale = models.CharField(max_length=200, choices=RETENTISSEMENT, default='1',null=True, blank=True)
    #Développement psychomoteur
    assis_avec_appui  = models.CharField(max_length=100, default="",null=True, blank=True)
    assis_sans_appui = models.CharField(max_length=100, default="",null=True, blank=True)
    marche_serpant = models.CharField(max_length=100, default="",null=True, blank=True)
    marche_4_pattes = models.CharField(max_length=100, default="",null=True, blank=True)
    debout_sans_appui = models.CharField(max_length=100, default="",null=True, blank=True)
    debout_avec_appui = models.CharField(max_length=100, default="",null=True, blank=True)
    parole_syllabe = models.CharField(max_length=100, default="",null=True, blank=True)
    parole_mots = models.CharField(max_length=100, default="",null=True, blank=True)
    parole_phrase = models.CharField(max_length=100, default="",null=True, blank=True)
    interaction_avec_entourage = models.CharField(max_length=100, default="Non",null=True, blank=True)
    trouble_de_concentration = models.CharField(max_length=100, default="Non",null=True, blank=True)
    trouble_de_comportement= models.CharField(max_length=100, default="Non",null=True, blank=True)
    spectre_autisme = models.CharField(max_length=100,default="Non",null=True, blank=True)
    #Caryotype
    caryotype = models.CharField(max_length=200, choices=CARYOTYPE, default='Non fait',null=True, blank=True)
    # Potentiel évoqué auditif fait
    potentiel_evoque_auditif = models.CharField(max_length=300, choices=POTENTIELAUDITIF, default='Non fait',null=True, blank=True)
    # Bilan thyroïdien fait
    bilan_thyroidien = models.CharField(max_length=100, default="Non",null=True, blank=True)
    # Pathologie endocrinienne
    pathologie_endocrinienne = models.CharField(max_length=200,default="",null=True, blank=True)
    age_pathologie_endocrinienne = models.CharField(max_length=100, default="",null=True, blank=True)
    diabete = models.CharField(max_length=100, default="Non",null=True, blank=True)
    age_diabete = models.CharField(max_length=100, default="",null=True, blank=True)
    obesite = models.CharField(max_length=100, default="Non",null=True, blank=True)
    imc = models.CharField(max_length=100, default="",null=True, blank=True)
    #Pathologie cardiaque
    echo_coeur_fait = models.CharField(max_length=300, default="Non",null=True, blank=True)
    echo_coeur_type = models.CharField(max_length=200, default="",null=True, blank=True)
    age_echocoeur_cardio = models.CharField(max_length=100, default="",null=True, blank=True)
    opere = models.CharField(max_length=100, default="Non",null=True, blank=True)
    suivi = models.CharField(max_length=100, default="Non",null=True, blank=True)
    commentairePCardiaque = models.TextField(null=True, blank=True)
    #Pathologie digestif
    reflux_gastro_oesophagien = models.CharField(max_length=100, default="Non",null=True, blank=True)
    maladie_coeliaque = models.CharField(max_length=100, default="Non",null=True, blank=True)
    mucoviscidose = models.CharField(max_length=100, default="Non",null=True, blank=True)
    agedebut_maladie_coalique = models.CharField(max_length=100, default="1",null=True, blank=True)
    #Hernies
    hernies = models.CharField(max_length=200, choices=HERNIS, default='1',null=True, blank=True)
    typeHernie_direction = models.CharField(max_length=200, default='',null=True, blank=True)
    #Pathologie ophtalmologique
    pathologie_ophtalmologique = models.TextField(null=True, blank=True)
    #Pathologie ORL
    pathologie_orl= models.TextField(null=True, blank=True)
    # Pathologie suivi dentaire
    pathologie_suivie_dentaire = models.CharField(max_length=500, default="Non",null=True, blank=True)
    pathologie_suivie_dentaire_Commentaire = models.TextField(null=True, blank=True)
    # Pathologie osteoarticulaire
    pathologie_osteoarticulaire = models.TextField(null=True, blank=True)
    # Pathologie neurologique
    pathologie_neurologique = models.TextField(null=True, blank=True)
    epilepsie = models.CharField(max_length=100, default="Non",null=True, blank=True)
    imagerie_faite = models.TextField(null=True, blank=True)
    #Autre pathologie
    autre_pathologie = models.TextField(null=True, blank=True)
    traitement = models.TextField(null=True, blank=True)
    #Pathologie respiratoire
    pathologie_respiratoire = models.TextField(null=True, blank=True)
    #Trouble digestif
    trouble_digestif = models.CharField(max_length=300, choices=TROUBLEDIGESTIF, default='1',null=True, blank=True)
    #Psychologue
    Psychologue_type = models.CharField(max_length=300, default="",null=True, blank=True)
    Psychologue_agedebut = models.CharField(max_length=100, default="",null=True, blank=True)
    Psychologue_frequenceensemaine = models.CharField(max_length=100, default="",null=True, blank=True)
    Psychologue_commentaire =  models.TextField(null=True, blank=True)
    #Orthophoniste
    Orthophoniste_type = models.CharField(max_length=300, default="",null=True, blank=True)
    Orthophoniste_agedebut = models.CharField(max_length=100, default="",null=True, blank=True)
    Orthophoniste_frequenceensemaine = models.CharField(max_length=100, default="",null=True, blank=True)
    Orthophoniste_commentaire = models.TextField(null=True, blank=True)
    #Psychomotricien
    Psychomotricien_type = models.CharField(max_length=300, default="",null=True, blank=True)
    Psychomotricien_agedebut = models.CharField(max_length=100, default="",null=True, blank=True)
    Psychomotricien_frequenceensemaine = models.CharField(max_length=100, default="",null=True, blank=True)
    Psychomotricien_commentaire = models.TextField(null=True, blank=True)
    #Kinesithérapie_fonctionnelle
    Kinesitherapie_fonctionnelle_type = models.CharField(max_length=300, default="",null=True, blank=True)
    Kinesitherapie_fonctionnelle_agedebut = models.CharField(max_length=100, default="",null=True, blank=True)
    Kinesitherapie_fonctionnelle_frequenceensemaine = models.CharField(max_length=100, default="",null=True, blank=True)
    Kinesitherapie_fonctionnelle_commentaire =  models.TextField(null=True, blank=True)
    # Orthoptiste
    Orthoptiste_type = models.CharField(max_length=300, default="",null=True, blank=True)
    Orthoptiste_agedebut = models.CharField(max_length=100, default="",null=True, blank=True)
    Orthoptiste_frequenceensemaine = models.CharField(max_length=100, default="",null=True, blank=True)
    Orthoptiste_commentaire =  models.TextField(null=True, blank=True)
    #Scolarite
    scolarise = models.CharField(max_length=100, default="Non",null=True, blank=True)
    scolarise_age_de_début = models.CharField(max_length=100, default="",null=True, blank=True)
    scolarise_classe_préparatoire = models.CharField(max_length=200, default="Non",null=True, blank=True)
    scolarise_bac_choice = models.CharField(max_length=100, default="Non",null=True, blank=True)
    scolarise_classe_secondaires_choice = models.CharField(max_length=100, default="Non",null=True, blank=True)
    scolarise_classe_primaire_choice = models.CharField(max_length=100, default="Non",null=True, blank=True)
    activite_sportive = models.CharField(max_length=100, default="Non",null=True, blank=True)
    activite_artistique = models.CharField(max_length=100, default="Non",null=True, blank=True)
    activite_prof = models.CharField(max_length=100, default="Non",null=True, blank=True)

    def __str__(self):
        return "Info-"+ str(self.patient)

class PathologieCardiqueOpere(models.Model):
    patientID = models.IntegerField(default=0)
    opere_date = models.CharField(max_length=300, default='',null=True, blank=True)
    opere_type = models.CharField(max_length=300, default='1',null=True, blank=True)
    opere_suivi = models.CharField(max_length=3, default="Non",null=True, blank=True)
    opere_suivi_date = models.CharField(max_length=300, default='', null=True, blank=True)

    def __str__(self):
        return "Opere-"+str(self.patientID)

class ObesiteImc(models.Model):
    patientID = models.IntegerField(default=0)
    obesite_date = models.DateField(null=True)
    obesite_poids = models.CharField(max_length=300, default='1',null=True, blank=True)
    obesite_taille = models.CharField(max_length=300, default='1',null=True, blank=True)
    imc = models.CharField(max_length=200, default='1',null=True, blank=True)

    def __str__(self):
        return "Obesite-"+str(self.patientID)

class PatientActivite(models.Model):
    patientID = models.IntegerField(default=0)
    type_activite = models.CharField(max_length=100, default="",null=True, blank=True)
    description_activite = models.CharField(max_length=100, default="",null=True, blank=True)
    def __str__(self):
        return str(self.patientID) + "-"+str(self.type_activite)

class PatientScolarite(models.Model):
    patientID = models.IntegerField(default=0)
    type_scolarite = models.CharField(max_length=100, default="",null=True, blank=True)
    level_scolarite = models.CharField(max_length=100, default="",null=True, blank=True)
    year_scolarite = models.CharField(max_length=100, default="",null=True, blank=True)

    def __str__(self):
        return str(self.patientID) + "-"+ str(self.level_scolarite)

class PathologieDentaire(models.Model):
    patientID = models.IntegerField(default=0)
    #date_act = models.DateField(null=True)
    date_act = models.CharField(max_length=100, default="01/01/2022", null=True)
    dent_GaucheDroit = models.CharField(max_length=50, default="G", null=True, blank=True)
    dent_HautBas = models.CharField(max_length=50, default="H", null=True, blank=True)
    dent_num = models.CharField(max_length=50, default="1", null=True, blank=True)
    code_act = models.CharField(max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return str(self.patientID) + "-"+ str(self.dent_GaucheDroit)+str(self.dent_HautBas)+str(self.dent_num)

class Delegation(models.Model):
    idDelegation = models.AutoField(primary_key=True)
    nomDelegation = models.CharField(max_length=100, unique=True, default="")
    def __str__(self):
        return str(self.nomDelegation)

class Ville(models.Model):
    idVille = models.AutoField(primary_key = True)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    nomVille = models.CharField(max_length=200,default="")

    def __str__(self):
        return str(self.nomVille)

class ClassePrimaire(models.Model):
    idClassePrimaire = models.AutoField(primary_key=True)
    classePName = models.CharField(max_length=100, unique=True, default="")

    def __str__(self):
        return str(self.classePName)

class ClasseSecondaire(models.Model):
    idClasseSecondaire = models.AutoField(primary_key=True)
    classeSName = models.CharField(max_length=100, unique=True, default="")

    def __str__(self):
        return str(self.classeSName)

class Mutuelle(models.Model):
    idMutuelle = models.AutoField(primary_key=True)
    mutuelleName = models.CharField(max_length=200, unique=True, default="")

    def __str__(self):
        return str(self.mutuelleName)