import os
import textwrap

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.staticfiles import finders
from reportlab.lib.colors import black
from reportlab.lib.units import mm, cm
from reportlab.lib.pagesizes import A5
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from django.db.models import Case, When, Q, Value, IntegerField
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import get_user_model
from Administrateur.models import *

User = get_user_model()


def home_patient(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        actualite = Actualite.objects.order_by('-post_date')[:8]
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        context = {
            'patient': patient,
            'imgPatient': img_path,
            'actualite': actualite,
        }
        return render(request, 'Patient/homeUser.html', context)
    else:
        return redirect('homPage')


def profile(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        context = {
            'patient': patient,
            'imgPatient': img_path,
        }
    return render(request, 'Patient/profile.html', context)


def update_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            patient = Patient.objects.get(pk=request.user.id)
            # Get the new values from the form
            numTelephoneMere = request.POST.get('numTelMere')
            numTelephonePere = request.POST.get('numTelPere')
            mailPatient = request.POST.get('mail')

            # Update the patient object with the new values
            patient.numTelephoneMere = numTelephoneMere
            patient.numTelephonePere = numTelephonePere
            patient.mailPatient = mailPatient
            patient.save()

            messages.success(request, "votre compte a été bien modifié")
            return redirect("profile")
    else:
        return redirect("profile")


class update_password(PasswordChangeView):
    template_name = 'Patient/password.html'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            patient = Patient.objects.get(user=self.request.user)
        except Patient.DoesNotExist:
            patient = None
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        context['patient'] = patient
        context['imgPatient'] = img_path
        return context


def password_success(request):
    messages.success(request, "votre mot de passe a été bien modifié")
    return redirect('update_password')


def infos_patient(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
            info = InfoPatient.objects.get(patient=patient)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        context = {
            'patient': patient,
            'imgPatient': img_path,
            'info': info,
        }
        return render(request, 'Patient/infosPatient.html', context)
    else:
        return redirect('loginUsers')


def imprimer_dossier_patient_pdf(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            patient = Patient.objects.get(user=request.user)
            patientInfo = InfoPatient.objects.get(patient=patient)
            patient_id = patient.idPatient
        except ObjectDoesNotExist:
            print("Impossible de trouver les informations sur le patient avec l'ID " + patient_id)
        else:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="' + str(patient_id) + '.pdf"'

            # Create the PDF object, using the buffer as its "file."
            pdf = canvas.Canvas(response, pagesize=A5)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            logo_path = finders.find('images/logoMinistre.jpg')
            if logo_path:
                pdf.drawImage(logo_path, 10 * mm, 190 * mm, 130 * mm, 20 * mm)
            else:
                print("Logo image not found")

            pdf.setFont("Helvetica-Bold", 14)
            r = int("41", 16)
            g = int("64", 16)
            b = int("4A", 16)
            pdf.setFillColorRGB(r / 255, g / 255, b / 255)
            text = 'DOSSIER MEDICAL'
            x = (pdf._pagesize[0] - pdf.stringWidth(text, "Helvetica-Bold", 13)) / 2.0
            pdf.drawString(x, 182 * mm, text)
            # Saute la ligne
            pdf.drawString(0, 182 * mm, "")

            width = 0
            height = 0
            pageNumber = 0
            # ----------------------Step 1 : Indormations personnels-----------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            data = [['Nom Prenom', str(patient.nomPatient) + " " + str(patient.prenomPatient)],
                    ['Sexe', str(patient.sexePatient)],
                    ['Date de naissance', str(patient.dateNaissancePatient)],
                    ['N° de télèphone de la mère', str(patient.numTelephoneMere)],
                    ['N° de télèphone du père', str(patient.numTelephonePere)],
                    ['Email', str(patient.mailPatient)],
                    ['Adresse', str(patient.delegationPatient) + ", " + str(patient.villePatient) + ", " + str(
                        patient.adressePatient)],
                    ['Couverture Médicale', str(patient.couvertureMedical) + ", " + str(patient.nomCouvertureMedical)],
                    ]
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, -1), 9),
                ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                ('BACKGROUND', (1, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

            table = Table(data)
            table.setStyle(table_style)

            # Titre du table
            text_color = HexColor('#2D2727')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(15, 490, "Identité du patient : ")

            table.wrapOn(pdf, 0, 0)
            height = height + 5
            width = width + 110
            table.drawOn(pdf, height * mm, width * mm)

            # ----------------------Step 2 : Dossier Antécédent-----------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            data = [['Parents Consanguins', str(patientInfo.parents_Consanguins)],
                    ["Age maternel à l'accouchement (en année)", str(patientInfo.age_maternel_accouchement)],
                    ['Grossesse suivi', str(patientInfo.grossesse_suivi)],
                    ['Terme de la grossesse', str(patientInfo.terme_grossesse)],
                    ['Précision du terme de la grossesse', str(patientInfo.precisionTerme)],
                    ['Accouchement par voie', str(patientInfo.accouchement_par_voie)],
                    ['Souffrance Néonatale', str(patientInfo.souffrance_neonatal)],
                    ['Poids de naissance (en Kg)', str(patientInfo.poids_de_naissance)],
                    ['Taille à la naissance (en cm)', str(patientInfo.taille_de_naissance)],
                    ["Hospitalisation à l'âge Néonatal", str(patientInfo.Notion_hospitalisation_age_neonatal)],
                    ['Allaitement', str(patientInfo.allaitement)],
                    ['Diversification Alimentaire à l’âge de (en mois)', str(patientInfo.diversification_alimentaire)],
                    ['Retentissement Staturo-Pondérale', str(patientInfo.retentissement_staturo_ponderale)],
                    ]
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, -1), 9),
                ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                ('BACKGROUND', (1, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)

            # Titre du table
            text_color = HexColor('#2D2727')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(15, 290, "Dossier Antécédent : ")

            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 5 * mm, 2 * mm)

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            # ----------------------Step 3 : Dossier médical-----------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # add new page
            pdf.showPage()
            text_color = HexColor('#2D2727')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(15, 570, "Dossier médical : ")

            ###################### Développement psychomoteur
            data = [['Assis avec appui (en mois)', str(patientInfo.assis_avec_appui)],
                    ["Assis sans appui (en mois)", str(patientInfo.assis_sans_appui)],
                    ['Marche au serpent (en mois)', str(patientInfo.marche_serpant)],
                    ['Marche à 4 pattes (en mois)', str(patientInfo.marche_4_pattes)],
                    ['Debout avec appui (en mois)', str(patientInfo.debout_avec_appui)],
                    ['Debout sans appui (en mois)', str(patientInfo.debout_sans_appui)],
                    ['Parole : Syllabe (en mois)', str(patientInfo.parole_syllabe)],
                    ['Parole : Mots (en mois)', str(patientInfo.parole_mots)],
                    ['Parole : Phrase (en mois)', str(patientInfo.parole_phrase)],
                    ["Trouble de comportement", str(patientInfo.trouble_de_comportement)],
                    ['Trouble de concentration', str(patientInfo.trouble_de_concentration)],
                    ['Interaction avec entourage', str(patientInfo.interaction_avec_entourage)],
                    ['Spectre autiste', str(patientInfo.spectre_autisme)],
                    ['Potentiel évoqué auditif fait', str(patientInfo.potentiel_evoque_auditif)],
                    ['Caryotype', str(patientInfo.caryotype)],
                    ['Bilan thyroïdien fait', str(patientInfo.bilan_thyroidien)],
                    ]
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, -1), 9),
                ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                ('BACKGROUND', (1, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 550, "Développement psychomoteur : ")
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 5 * mm, 72 * mm)

            ###################### Pathologie digestive
            data = [['Reflux gastro-oesophagien', str(patientInfo.reflux_gastro_oesophagien)],
                    ["Maladie coeliaque", str(patientInfo.maladie_coeliaque)],
                    ["Age de la maladie coeliaque", str(patientInfo.agedebut_maladie_coalique)],
                    ["Mucoviscidose", str(patientInfo.mucoviscidose)],
                    ]
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, -1), 9),
                ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                ('BACKGROUND', (1, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (1, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 190, "Pathologie digestive : ")
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 5 * mm, 35 * mm)

            ###################### Hernies
            data = [['Hernies', str(patientInfo.hernies)],
                    ["Type d'hernies", str(patientInfo.typeHernie_direction)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 35)

            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 85, "Hernies : ")

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            ###################### Pathologie cardiaque
            pdf.showPage()

            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 570, "Pathologie cardiaque : ")

            data = [['Dernier echocoeur', str(patientInfo.echo_coeur_fait)],
                    ["Précision de type d'echocoeur", str(patientInfo.echo_coeur_type)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 520)

            table_style1 = TableStyle([
                ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # ------ opéré
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, 500, "Opéré : ")

            data = [['Opéré', str(patientInfo.opere)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 470)

            y = 460
            if (patientInfo.opere == "Oui"):
                opere = []
                opere_dates = []
                opere_types = []

                if (patientInfo.opere == "Oui"):
                    patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
                    for x in patientOpereCardiaque:
                        opere_dates.append(x.opere_date)
                        opere_types.append(x.opere_type)

                data = [["Date d'opération", "Type d'opération"],
                        ]
                col_widths = [6.5 * cm, 6.5 * cm]
                table = Table(data, colWidths=col_widths)
                table.setStyle(table_style1)
                table.wrapOn(pdf, 0, 0)
                table.drawOn(pdf, 15, 440)

                y = 440
                for i in range(0, len(opere_dates)):
                    y = y - 21
                    row = [[opere_dates[i], opere_types[i]], ]
                    table = Table(row, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

            # ------ suivi
            y = y - 18
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Suivi : ")

            y = y - 27
            data = [['Suivi', str(patientInfo.suivi)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 27
            if (patientInfo.suivi == "Oui"):
                suivi = []
                suivi_dates = []
                suivi_types = []

                if (patientInfo.suivi == "Oui"):
                    patientSuiviCardiaque = PathologieCardiqueSuivi.objects.filter(patientID=patient_id)
                    for x in patientSuiviCardiaque:
                        suivi_dates.append(x.suivi_date)
                        suivi_types.append(x.suivi_type)

                data = [["Date de suivi", "Type de suivi"],
                        ]
                col_widths = [6.5 * cm, 6.5 * cm]
                table = Table(data, colWidths=col_widths)
                table.setStyle(table_style1)
                table.wrapOn(pdf, 0, 0)
                table.drawOn(pdf, 15, y)

                for i in range(0, len(suivi_dates)):
                    y = y - 21
                    row = [[suivi_dates[i], suivi_types[i]], ]
                    table = Table(row, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

            # ---Commentaire
            y = y - 18
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            max_width = 840
            font_size = 10
            font_name = 'Helvetica'
            lines = textwrap.wrap(patientInfo.commentairePCardiaque, width=max_width // font_size)
            pdf.setFont(font_name, font_size)
            for line in lines:
                pdf.drawString(15, y, line)
                y -= leading

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            ###################### Pathologie endocrinienne
            pdf.showPage()

            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 570, "Pathologie endocrinienne : ")

            data = [['Pathologie endocrinienne thyroïdienne', str(patientInfo.pathologie_endocrinienne)],
                    ["Précision d'âge", str(patientInfo.age_pathologie_endocrinienne)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 520)

            data = [['Diabète', str(patientInfo.diabete)],
                    ["Précision d'âge", str(patientInfo.age_diabete)],
                    ]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 470)

            # ------obésité
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, 457, "Obésité : ")

            data = [['Obésité', str(patientInfo.obesite)],
                    ]
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, 430)

            y = 400
            if (patientInfo.obesite == "Oui"):
                obesite_dates = []
                obesite_poids = []
                obesite_tailles = []
                obesite_imc = []

                if (patientInfo.opere == "Oui"):
                    patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
                    for x in patientObeseteImc:
                        obesite_dates.append(x.obesite_date)
                        obesite_poids.append(x.obesite_poids)
                        obesite_tailles.append(x.obesite_taille)
                        obesite_imc.append(x.imc)

                obesite = [['Date', 'Poids (en Kg)', 'Taille (en cm)', 'IMC'],
                           ]
                col_widths = [3 * cm, 3 * cm, 3 * cm, 3 * cm]
                table = Table(obesite, colWidths=col_widths)
                table.setStyle(table_style1)
                table.wrapOn(pdf, 0, 0)
                table.drawOn(pdf, 15, y)

                for i in range(0, len(obesite_dates)):
                    y = y - 21
                    row = [[obesite_dates[i], obesite_poids[i], obesite_tailles[i], obesite_imc[i]], ]
                    table = Table(row, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

            ###################### Pathologie ophtalmologique
            y = y - 21
            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Pathologie ophtalmologique : ")
            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.pathologie_ophtalmologique != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.pathologie_ophtalmologique,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            ###################### Pathologie ORL
            y = y - 10
            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Pathologie ORL : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.pathologie_orl != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.pathologie_orl,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            ###################### Pathologie suivi dentaire
            pdf.showPage()

            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 570, "Pathologie suivi dentaire : ")

            y = 570
            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.pathologie_suivie_dentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.pathologie_suivie_dentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            ###################### Pathologie endocrinienne
            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Pathologie osteoarticulaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.pathologie_osteoarticulaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.pathologie_osteoarticulaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            ###################### Pathologie endocrinienne
            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Pathologie neurologique : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.pathologie_neurologique != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.pathologie_neurologique,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ------Epilepsie
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Epilepsie : ")
            data = [['Epilepsie', str(patientInfo.epilepsie)],
                    ]
            y = y - 30
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20

            # ------Imagerie faite
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Imagerie faite : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.imagerie_faite != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.imagerie_faite,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            ###################### Autre Pathologie
            pdf.showPage()
            # Titre du table
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 570, "Autre Pathologie : ")

            y = 570
            y = y - 18
            # ------Autre Pathologie
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Autre Pathologie : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.autre_pathologie != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.autre_pathologie,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ------Traitement
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Traitement : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.traitement != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.traitement,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ----------------------Step 4 : Suivi médical-----------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            text_color = HexColor('#2D2727')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(15, y, "Suivi médical : ")

            # ------Suivi médical : Psychomotricien
            y = y - 18
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Suivi médical : Psychomotricien  ")

            data = [['Type', str(patientInfo.Psychomotricien_type)],
                    ['Âge de début', str(patientInfo.Psychomotricien_agedebut)],
                    ['Fréquence en semaine', str(patientInfo.Psychomotricien_frequenceensemaine)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.Psychomotricien_commentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.Psychomotricien_commentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            # ------Suivi médical : Kinesitherapie_fonctionnelle
            pdf.showPage()
            y = 570
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, 570, "Suivi médical : Kinésithérapie fonctionnelle  ")

            data = [['Type', str(patientInfo.Kinesitherapie_fonctionnelle_type)],
                    ['Âge de début', str(patientInfo.Kinesitherapie_fonctionnelle_agedebut)],
                    ['Fréquence en semaine', str(patientInfo.Kinesitherapie_fonctionnelle_frequenceensemaine)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.Kinesitherapie_fonctionnelle_commentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.Kinesitherapie_fonctionnelle_commentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ------Suivi médical : Psychologue
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Suivi médical : Psychologue  ")

            data = [['Type', str(patientInfo.Psychologue_type)],
                    ['Âge de début', str(patientInfo.Psychologue_agedebut)],
                    ['Fréquence en semaine', str(patientInfo.Psychologue_frequenceensemaine)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.Psychologue_commentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.Psychologue_commentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ------Suivi médical : Orthophoniste
            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            pdf.showPage()
            y = 570
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Suivi médical : Orthophoniste  ")

            data = [['Type', str(patientInfo.Orthophoniste_type)],
                    ['Âge de début', str(patientInfo.Orthophoniste_agedebut)],
                    ['Fréquence en semaine', str(patientInfo.Orthophoniste_frequenceensemaine)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.Orthophoniste_commentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.Orthophoniste_commentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ------Suivi médical : Orthoptiste
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Suivi médical : Orthoptiste  ")

            data = [['Type', str(patientInfo.Orthoptiste_type)],
                    ['Âge de début', str(patientInfo.Orthoptiste_agedebut)],
                    ['Fréquence en semaine', str(patientInfo.Orthoptiste_frequenceensemaine)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            y = y - 20
            text_color = HexColor('#93BFCF')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(15, y, "Commentaire : ")

            y = y - 18
            pdf.setFillColor(colors.black)
            leading = 18
            if patientInfo.Orthoptiste_commentaire != "":
                max_width = 840
                font_size = 10
                font_name = 'Helvetica'
                lines = textwrap.wrap(patientInfo.Orthoptiste_commentaire,
                                      width=max_width // font_size)
                pdf.setFont(font_name, font_size)
                for line in lines:
                    pdf.drawString(15, y, line)
                    y -= leading
            else:
                text = ['a', 'b', 'c', 'd']
                for x in text:
                    pdf.drawString(15, y, "     ")
                    y -= leading

            # ----------------------Step 5 : Scolarité et activités-----------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------
            pageNumber = pageNumber + 1
            text_color = HexColor('#212A3E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica", 10)
            pdf.drawString(408, 10, str(pageNumber))

            y = 570
            pdf.showPage()
            text_color = HexColor('#2D2727')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(15, y, "Scolarité et activités : ")

            y = y - 21
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Scolarité : ")

            data = [['Scolarisé', str(patientInfo.scolarise)],
                    ['Âge de début', str(patientInfo.scolarise_age_de_début)],
                    ['Classe préparatoire', str(patientInfo.scolarise_classe_préparatoire)],
                    ]
            y = y - 70
            col_widths = [8 * cm, 5 * cm]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            table.wrapOn(pdf, 0, 0)
            table.drawOn(pdf, 15, y)

            # ------scolarite
            if patientInfo.scolarise == "Oui":
                classePS = [['Classe', 'Année scolaire'],
                            ]
                classeB = [['Filiére', 'Année scolaire'],
                           ]

                if (patientInfo.scolarise_classe_primaire_choice == "on"):
                    classe_primaires = []
                    classe_primaire_years = []

                    y = y - 18
                    text_color = HexColor('#93BFCF')
                    pdf.setFillColor(text_color)
                    pdf.setFont("Helvetica-Bold", 11)
                    pdf.drawString(15, y, "Classes primaires : ")
                    y = y - 25
                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="Classe primaire")
                    for x in patientScolarite:
                        classe_primaires.append(x.level_scolarite)
                        classe_primaire_years.append(x.year_scolarite)

                    col_widths = [6.5 * cm, 6.5 * cm]
                    table = Table(classePS, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

                    for i in range(0, len(classe_primaires)):
                        y = y - 21
                        if (y < 20):
                            pageNumber = pageNumber + 1
                            text_color = HexColor('#212A3E')
                            pdf.setFillColor(text_color)
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(408, 10, str(pageNumber))

                            pdf.showPage()
                            y = 570
                        row = [[classe_primaires[i], classe_primaire_years[i]], ]
                        table = Table(row, colWidths=col_widths)
                        table.setStyle(table_style1)
                        table.wrapOn(pdf, 0, 0)
                        table.drawOn(pdf, 15, y)

                if (patientInfo.scolarise_classe_secondaires_choice == "on"):
                    if (y < 20):
                        pageNumber = pageNumber + 1
                        text_color = HexColor('#212A3E')
                        pdf.setFillColor(text_color)
                        pdf.setFont("Helvetica", 10)
                        pdf.drawString(408, 10, str(pageNumber))

                        pdf.showPage()
                        y = 570
                    classe_secondaires = []
                    classe_secondaire_years = []
                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="Classe secondaire")
                    for x in patientScolarite:
                        classe_secondaires.append(x.level_scolarite)
                        classe_secondaire_years.append(x.year_scolarite)

                    y = y - 18
                    text_color = HexColor('#93BFCF')
                    pdf.setFillColor(text_color)
                    pdf.setFont("Helvetica-Bold", 11)
                    pdf.drawString(15, y, "Classes secondaires : ")
                    y = y - 25

                    col_widths = [6.5 * cm, 6.5 * cm]
                    table = Table(classePS, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

                    for i in range(0, len(classe_secondaires)):
                        y = y - 21
                        if (y < 20):
                            pageNumber = pageNumber + 1
                            text_color = HexColor('#212A3E')
                            pdf.setFillColor(text_color)
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(408, 10, str(pageNumber))

                            pdf.showPage()
                            y = 570
                        row = [[classe_secondaires[i], classe_secondaire_years[i]], ]
                        table = Table(row, colWidths=col_widths)
                        table.setStyle(table_style1)
                        table.wrapOn(pdf, 0, 0)
                        table.drawOn(pdf, 15, y)

                if (patientInfo.scolarise_bac_choice == "on"):
                    if (y < 20):
                        pageNumber = pageNumber + 1
                        text_color = HexColor('#212A3E')
                        pdf.setFillColor(text_color)
                        pdf.setFont("Helvetica", 10)
                        pdf.drawString(408, 10, str(pageNumber))

                        pdf.showPage()
                        y = 570
                    bac_filieres = []
                    bac_years = []

                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="BAC")
                    for x in patientScolarite:
                        bac_filieres.append(x.level_scolarite)
                        bac_years.append(x.year_scolarite)

                    y = y - 18
                    text_color = HexColor('#93BFCF')
                    pdf.setFillColor(text_color)
                    pdf.setFont("Helvetica-Bold", 11)
                    pdf.drawString(15, y, "BAC : ")
                    y = y - 25

                    col_widths = [6.5 * cm, 6.5 * cm]
                    table = Table(classeB, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

                    for i in range(0, len(bac_filieres)):
                        y = y - 21
                        if (y < 20):
                            pageNumber = pageNumber + 1
                            text_color = HexColor('#212A3E')
                            pdf.setFillColor(text_color)
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(408, 10, str(pageNumber))

                            pdf.showPage()
                            y = 570
                        row = [[bac_filieres[i], bac_years[i]], ]
                        table = Table(row, colWidths=col_widths)
                        table.setStyle(table_style1)
                        table.wrapOn(pdf, 0, 0)
                        table.drawOn(pdf, 15, y)
                        ##########################
                        # --------------activités
                        y = y - 21
                        text_color = HexColor('#6B728E')
                        pdf.setFillColor(text_color)
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(15, y, "Activités : ")
                        y = y - 25

                        if (patientInfo.activite_sportive == "Oui"
                                or patientInfo.activite_artistique == "Oui"
                                or patientInfo.activite_prof == "Oui"):

                            if (y < 20):
                                pageNumber = pageNumber + 1
                                text_color = HexColor('#212A3E')
                                pdf.setFillColor(text_color)
                                pdf.setFont("Helvetica", 10)
                                pdf.drawString(408, 10, str(pageNumber))

                                pdf.showPage()
                                y = 570

                            type_activite = []
                            description_activite = []
                            activiteHeader = [["Type d'activité", "Description d'activité"], ]

                            patientActivite = PatientActivite.objects.filter(patientID=patient_id)
                            for x in patientActivite:
                                type_activite.append(x.type_activite)
                                description_activite.append(x.description_activite)

                            col_widths = [6.5 * cm, 6.5 * cm]
                            table = Table(activiteHeader, colWidths=col_widths)
                            table.setStyle(table_style1)
                            table.wrapOn(pdf, 0, 0)
                            table.drawOn(pdf, 15, y)

                            for i in range(0, len(type_activite)):
                                y = y - 21
                                if (y < 20):
                                    pageNumber = pageNumber + 1
                                    text_color = HexColor('#212A3E')
                                    pdf.setFillColor(text_color)
                                    pdf.setFont("Helvetica", 10)
                                    pdf.drawString(408, 10, str(pageNumber))

                                    pdf.showPage()
                                    y = 570
                                row = [[type_activite[i], description_activite[i]], ]
                                table = Table(row, colWidths=col_widths)
                                table.setStyle(table_style1)
                                table.wrapOn(pdf, 0, 0)
                                table.drawOn(pdf, 15, y)

                            pageNumber = pageNumber + 1
                            text_color = HexColor('#212A3E')
                            pdf.setFillColor(text_color)
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(408, 10, str(pageNumber))

            # --------------activités
            y = y - 21
            text_color = HexColor('#6B728E')
            pdf.setFillColor(text_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(15, y, "Activités : ")
            y = y - 25

            if (patientInfo.activite_sportive == "Oui"
                    or patientInfo.activite_artistique == "Oui"
                    or patientInfo.activite_prof == "Oui"):

                if (y < 20):
                    pageNumber = pageNumber + 1
                    text_color = HexColor('#212A3E')
                    pdf.setFillColor(text_color)
                    pdf.setFont("Helvetica", 10)
                    pdf.drawString(408, 10, str(pageNumber))

                    pdf.showPage()
                    y = 570

                type_activite = []
                description_activite = []
                activiteHeader = [["Type d'activité", "Description d'activité"], ]

                patientActivite = PatientActivite.objects.filter(patientID=patient_id)
                for x in patientActivite:
                    type_activite.append(x.type_activite)
                    description_activite.append(x.description_activite)

                col_widths = [6.5 * cm, 6.5 * cm]
                table = Table(activiteHeader, colWidths=col_widths)
                table.setStyle(table_style1)
                table.wrapOn(pdf, 0, 0)
                table.drawOn(pdf, 15, y)

                for i in range(0, len(type_activite)):
                    y = y - 21
                    if (y < 20):
                        pageNumber = pageNumber + 1
                        text_color = HexColor('#212A3E')
                        pdf.setFillColor(text_color)
                        pdf.setFont("Helvetica", 10)
                        pdf.drawString(408, 10, str(pageNumber))

                        pdf.showPage()
                        y = 570
                    row = [[type_activite[i], description_activite[i]], ]
                    table = Table(row, colWidths=col_widths)
                    table.setStyle(table_style1)
                    table.wrapOn(pdf, 0, 0)
                    table.drawOn(pdf, 15, y)

                pageNumber = pageNumber + 1
                text_color = HexColor('#212A3E')
                pdf.setFillColor(text_color)
                pdf.setFont("Helvetica", 10)
                pdf.drawString(408, 10, str(pageNumber))

            ####################################################################################
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            # Close the PDF object cleanly, and we're done.
        pdf.save()
        return response
    else:
        return redirect('loginUsers')


def logout_patient(request):
    if request.user.is_authenticated:
        try:
            logout(request)
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
            render(request, 'Patient/homeUser.html', {'error': error, 'errorValue': errorValue})
        else:
            return redirect("home_patient")
    else:
        return redirect('homPage')
