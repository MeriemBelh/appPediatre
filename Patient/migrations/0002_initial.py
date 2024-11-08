# Generated by Django 4.1.6 on 2023-05-29 23:50

import Patient.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pediatre', '0001_initial'),
        ('Patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('idPatient', models.IntegerField(default=Patient.models.get_and_update_generate_id, unique=True)),
                ('passwordPatient', models.CharField(max_length=100, null=True)),
                ('sexePatient', models.CharField(default='Unisexe', max_length=100, null=True)),
                ('nomPatient', models.CharField(max_length=60, null=True)),
                ('prenomPatient', models.CharField(max_length=60, null=True)),
                ('dateNaissancePatient', models.DateField(null=True)),
                ('mailPatient', models.EmailField(max_length=254, null=True)),
                ('adressePatient', models.TextField(max_length=300, null=True)),
                ('numTelephoneMere', models.IntegerField(null=True)),
                ('numTelephonePere', models.IntegerField(null=True)),
                ('villePatient', models.CharField(max_length=100, null=True)),
                ('delegationPatient', models.CharField(max_length=100, null=True)),
                ('couvertureMedical', models.CharField(max_length=200, null=True)),
                ('nomCouvertureMedical', models.CharField(default='', max_length=200, null=True)),
                ('imgPatient', models.ImageField(blank=True, default=Patient.models.default_image, upload_to='imgProfile_patient/')),
                ('is_deleted', models.CharField(default='Non', max_length=3)),
                ('inpe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Pediatre.pediatre')),
            ],
        ),
        migrations.CreateModel(
            name='PatientActivite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.IntegerField(default=0)),
                ('type_activite', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('description_activite', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientScolarite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.IntegerField(default=0)),
                ('type_scolarite', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('level_scolarite', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('year_scolarite', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CorbeillePatient',
            fields=[
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Patient.patient')),
                ('dateSuppression_debut', models.DateField(default=datetime.datetime(2023, 5, 29, 23, 50, 6))),
                ('dateSuppression_fin', models.DateField(default=datetime.datetime(2023, 6, 29, 0, 50, 6))),
            ],
        ),
        migrations.CreateModel(
            name='InfoPatient',
            fields=[
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Patient.patient')),
                ('parents_Consanguins', models.CharField(blank=True, default='Non', max_length=20, null=True)),
                ('age_maternel_accouchement', models.IntegerField(blank=True, default=100, null=True)),
                ('grossesse_suivi', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('terme_grossesse', models.CharField(blank=True, choices=[('1', 'A terme'), ('2', 'Prématuré')], default='1', max_length=200, null=True)),
                ('precisionTerme', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('accouchement_par_voie', models.CharField(blank=True, choices=[('1', 'Basse'), ('2', 'Césarienne')], default='1', max_length=200, null=True)),
                ('souffrance_neonatal', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('poids_de_naissance', models.CharField(blank=True, choices=[('1', '< 2Kg'), ('2', '2--2,5Kg'), ('3', '2,5--4Kg'), ('4', '> 4Kg')], default='1', max_length=100, null=True)),
                ('taille_de_naissance', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Notion_hospitalisation_age_neonatal', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('allaitement', models.CharField(blank=True, choices=[('1', 'Maternel'), ('2', 'Mixte'), ('3', 'Artificiel')], default='1', max_length=100, null=True)),
                ('diversification_alimentaire', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('retentissement_staturo_ponderale', models.CharField(blank=True, choices=[('1', 'Retard'), ('2', 'Stagnation'), ('3', 'Bon')], default='1', max_length=200, null=True)),
                ('assis_avec_appui', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('assis_sans_appui', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('marche_serpant', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('marche_4_pattes', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('debout_sans_appui', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('debout_avec_appui', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('parole_syllabe', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('parole_mots', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('parole_phrase', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('interaction_avec_entourage', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('trouble_de_concentration', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('trouble_de_comportement', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('spectre_autisme', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('caryotype', models.CharField(blank=True, choices=[('NonFait', 'Non fait'), ('Fait', (('1', 'Libre et homogène'), ('2', 'Mosaique'), ('3', 'Partielle'), ('4', 'Translocation')))], default='Non fait', max_length=200, null=True)),
                ('potentiel_evoque_auditif', models.CharField(blank=True, choices=[('1', 'Normaux'), ('2', 'Surdité totale'), ('3', 'Surdité partielle')], default='Non fait', max_length=300, null=True)),
                ('bilan_thyroidien', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('pathologie_endocrinienne', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('age_pathologie_endocrinienne', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('diabete', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('age_diabete', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('obesite', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('imc', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('echo_coeur_fait', models.CharField(blank=True, default='Non', max_length=300, null=True)),
                ('echo_coeur_type', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('age_echocoeur_cardio', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('opere', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('suivi', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('commentairePCardiaque', models.TextField(blank=True, null=True)),
                ('reflux_gastro_oesophagien', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('maladie_coeliaque', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('mucoviscidose', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('agedebut_maladie_coalique', models.CharField(blank=True, default='1', max_length=100, null=True)),
                ('hernies', models.CharField(blank=True, choices=[('1', 'Aucune'), ('2', 'Ombilical'), ('3', 'Inguinale')], default='1', max_length=200, null=True)),
                ('typeHernie_direction', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('pathologie_ophtalmologique', models.TextField(blank=True, null=True)),
                ('pathologie_orl', models.TextField(blank=True, null=True)),
                ('pathologie_suivie_dentaire', models.CharField(blank=True, default='Non', max_length=500, null=True)),
                ('pathologie_suivie_dentaire_Commentaire', models.TextField(blank=True, null=True)),
                ('pathologie_osteoarticulaire', models.TextField(blank=True, null=True)),
                ('pathologie_neurologique', models.TextField(blank=True, null=True)),
                ('epilepsie', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('imagerie_faite', models.TextField(blank=True, null=True)),
                ('autre_pathologie', models.TextField(blank=True, null=True)),
                ('traitement', models.TextField(blank=True, null=True)),
                ('pathologie_respiratoire', models.TextField(blank=True, null=True)),
                ('trouble_digestif', models.CharField(blank=True, choices=[('1', 'Constipation'), ('2', 'Diarrhée'), ('3', 'Normal')], default='1', max_length=300, null=True)),
                ('Psychologue_type', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('Psychologue_agedebut', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Psychologue_frequenceensemaine', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Psychologue_commentaire', models.TextField(blank=True, null=True)),
                ('Orthophoniste_type', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('Orthophoniste_agedebut', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Orthophoniste_frequenceensemaine', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Orthophoniste_commentaire', models.TextField(blank=True, null=True)),
                ('Psychomotricien_type', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('Psychomotricien_agedebut', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Psychomotricien_frequenceensemaine', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Psychomotricien_commentaire', models.TextField(blank=True, null=True)),
                ('Kinesitherapie_fonctionnelle_type', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('Kinesitherapie_fonctionnelle_agedebut', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Kinesitherapie_fonctionnelle_frequenceensemaine', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Kinesitherapie_fonctionnelle_commentaire', models.TextField(blank=True, null=True)),
                ('Orthoptiste_type', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('Orthoptiste_agedebut', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Orthoptiste_frequenceensemaine', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('Orthoptiste_commentaire', models.TextField(blank=True, null=True)),
                ('scolarise', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('scolarise_age_de_début', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('scolarise_classe_préparatoire', models.CharField(blank=True, default='Non', max_length=200, null=True)),
                ('scolarise_bac_choice', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('scolarise_classe_secondaires_choice', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('scolarise_classe_primaire_choice', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('activite_sportive', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('activite_artistique', models.CharField(blank=True, default='Non', max_length=100, null=True)),
                ('activite_prof', models.CharField(blank=True, default='Non', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('idVille', models.AutoField(primary_key=True, serialize=False)),
                ('nomVille', models.CharField(default='', max_length=200)),
                ('delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.delegation')),
            ],
        ),
    ]
