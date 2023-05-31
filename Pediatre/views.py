import io
import json
import os
import textwrap
from datetime import datetime
from urllib.parse import urlparse

from dateutil.relativedelta import relativedelta
from django.contrib.staticfiles import finders
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from django.db.models import Case, When, Q, Value, IntegerField

from .forms import *
from Patient.models import *
from Administrateur.models import *
from Pediatre.models import *
from AppPediatre.views import *

from AppPediatre import settings

from django.contrib.auth import get_user_model
User = get_user_model()


def imprimer_dossier_patient_pdf(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            patientInfo = InfoPatient.objects.get(patient=patient)
            patientActivite = PatientActivite.objects.filter(patientID=patient_id)
            patientScolarite = PatientScolarite.objects.filter(patientID=patient_id)
            patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
            patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
        except ObjectDoesNotExist:
            errorMessage = "Impossible de trouver les informations sur le patient avec l'ID " + str(patient_id)
            errorValue = True
            url = reverse('home_pediatre') + f'?error={errorMessage}&errorValue={errorValue}'
            return redirect(url)
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
                opere_suivis = []
                opere_suivi_dates = []

                if (patientInfo.opere == "Oui"):
                    patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
                    for x in patientOpereCardiaque:
                        opere_dates.append(x.opere_date)
                        opere_types.append(x.opere_type)
                        opere_suivis.append(x.opere_suivi)
                        opere_suivi_dates.append(x.opere_suivi_date)

                data = [["Date d'opération", "Type d'opération", "Suivi", "Date du suivi"],
                        ]
                col_widths = [3 * cm, 3 * cm, 3 * cm, 3 * cm]
                table = Table(data, colWidths=col_widths)
                table.setStyle(table_style1)
                table.wrapOn(pdf, 0, 0)
                table.drawOn(pdf, 15, 440)

                y = 440
                for i in range(0, len(opere_dates)):
                    y = y - 21
                    row = [[opere_dates[i], opere_types[i], opere_suivis[i], opere_suivi_dates[i]], ]
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



        ####################################################################################
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        # Close the PDF object cleanly, and we're done.
        pdf.save()
        return response
    else:
        return redirect('login_pediatre')


def modifier_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        submitted = False
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            userPatient = User.objects.get(username=patient_id)
            patientInfo = InfoPatient.objects.get(patient=patient)

            # Declaration des vars
            classe_primaires = []
            classe_primaire_years = []
            classe_secondaires = []
            classe_secondaire_years = []
            bac_years = []
            bac_filieres = []
            ASp = []
            APr = []
            AAr = []
            opere_dates = []
            opere_types = []
            opere_suivis = []
            opere_suivi_dates = []
            obesite_dates = []
            obesite_poids = []  # kg
            obesite_taille = []  # cm (1/100 pour m)
            imcs = []
            dates_acts = []
            dent_GaucheDroits = []
            dent_HautBass = []
            dent_nums = []
            codes_acts = []

            if (patientInfo.pathologie_suivie_dentaire == "Oui"):
                patientDentaire = PathologieDentaire.objects.filter(patientID=patient_id)
                for x in patientDentaire:
                    dates_acts.append(x.date_act)
                    dent_GaucheDroits.append(x.dent_GaucheDroit)
                    dent_HautBass.append(x.dent_HautBas)
                    dent_nums.append(x.dent_num)
                    codes_acts.append(x.code_act)

            if (patientInfo.opere == "Oui"):
                patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
                for x in patientOpereCardiaque:
                    opere_dates.append(x.opere_date)
                    opere_types.append(x.opere_type)
                    opere_suivis.append(x.opere_suivi)
                    opere_suivi_dates.append(x.opere_suivi_date)

            if (patientInfo.obesite == "Oui"):
                patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
                for x in patientObeseteImc:
                    obesite_dates.append(x.obesite_date.strftime('%Y-%m-%d'))
                    obesite_poids.append(x.obesite_poids)
                    obesite_taille.append(x.obesite_taille)
                    imcs.append(x.imc)

            if (patientInfo.scolarise == "Oui"):
                # classe_primaire_years classe_primaires
                if patientInfo.scolarise_classe_primaire_choice == "on":
                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="Classe primaire")
                    for x in patientScolarite:
                        classe_primaires.append(x.level_scolarite)
                        classe_primaire_years.append(x.year_scolarite)

                # "Classe secondaire" classe_secondaire_years classe_secondaires
                if patientInfo.scolarise_classe_secondaires_choice == "on":
                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="Classe secondaire")
                    for x in patientScolarite:
                        classe_secondaires.append(x.level_scolarite)
                        classe_secondaire_years.append(x.year_scolarite)

                # "BAC" bac_years bac_filieres
                if patientInfo.scolarise_bac_choice == "on":
                    patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                       type_scolarite="BAC")
                    for x in patientScolarite:
                        bac_filieres.append(x.level_scolarite)
                        bac_years.append(x.year_scolarite)

            if (patientInfo.activite_sportive == "Oui"):
                patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                 type_activite="Activite sportive")
                for x in patientActivite:
                    ASp.append(x.description_activite)

            if (patientInfo.activite_artistique == "Oui"):
                patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                 type_activite="Activite artistique")
                for x in patientActivite:
                    AAr.append(x.description_activite)

            if (patientInfo.activite_prof == "Oui"):
                patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                 type_activite="Activite professionnel")
                for x in patientActivite:
                    APr.append(x.description_activite)

        except BaseException as e:
            error = str(e)
            errorValue = True
            return redirect('home_pediatre/?error=' + error + '&errorValue=' + str(errorValue))
        else:
            classePrimaireT = []
            classeSecondaireT = []
            classeBacT = []
            for i in range(0, len(classe_primaires)):
                classePrimaireT.append([classe_primaires[i], classe_primaire_years[i]])

            for i in range(0, len(classe_secondaires)):
                classeSecondaireT.append([classe_secondaires[i], classe_secondaire_years[i]])

            for i in range(0, len(bac_filieres)):
                classeBacT.append([bac_years[i], bac_filieres[i]])

            yearsScolarite = []
            for number in range(datetime.now().year, 1988, -1):
                yearsScolarite.append(str(number) + "/" + str(number - 1))

            yearsScolarite_one = []
            for number in range(datetime.now().year, 1988, -1):
                yearsScolarite_one.append(str(number))

            suiviDentaireInfos = []
            for i in range(0, len(dates_acts)):
                suiviDentaireInfos.append([dates_acts[i], dent_GaucheDroits[i],dent_HautBass[i],dent_nums[i], codes_acts[i]])

            opereInfos = []
            for i in range(0, len(opere_dates)):
                opereInfos.append([opere_dates[i], opere_types[i], opere_suivis[i], opere_suivi_dates[i]])

            obesiteInfos = []
            for i in range(0, len(obesite_dates)):
                obesiteInfos.append([obesite_dates[i], obesite_poids[i], obesite_taille[i]])

            regions = Delegation.objects.values_list('nomDelegation', flat=True)
            villes = Ville.objects.values_list('nomVille', flat=True)
            POIDSNAISSANCE = [
                "< 2Kg",
                "2--2,5Kg",
                "2,5--4Kg",
                "> 4Kg"
            ]
            ALLAITEMENT = [
                "Maternel",
                "Mixte",
                "Artificiel",
            ]
            RETENTISSEMENT = [
                "Retard",
                "Stagnation",
                "Bon",
            ]
            POTENTIELAUDITIF = [
                "Normaux",
                "Surdité totale",
                "Surdité partielle",
            ]
            CARYOTYPE = [
                'Libre et homogène',
                'Mosaique',
                'Partielle',
                'Translocation',
            ]
            TROUBLEDIGESTIF = [
                "Constipation",
                "Diarrhée",
                "Normal",
            ]
            CPr = ClassePrimaire.objects.values_list('classePName', flat=True)
            CSr = ClasseSecondaire.objects.values_list('classeSName', flat=True)
            mutuelles = Mutuelle.objects.values_list('mutuelleName', flat=True).order_by('mutuelleName')
            numDents8 = ['1','2','3','4','5','6','7','8']
            context = {
                'mutuelles': list(mutuelles),
                'numDents8': list(numDents8),
                'opereInfos': opereInfos,
                'obesiteInfos': obesiteInfos,
                'yearsScolarite_one': yearsScolarite_one,
                'yearsScolarite': yearsScolarite,
                'CPr': list(CPr),
                'CSr': list(CSr),
                'classePrimaireT': classePrimaireT,
                'classeSecondaireT': classeSecondaireT,
                'classeBacT': classeBacT,
                'TROUBLEDIGESTIF': TROUBLEDIGESTIF,
                'POIDSNAISSANCE': POIDSNAISSANCE,
                'ALLAITEMENT': ALLAITEMENT,
                'CARYOTYPE': CARYOTYPE,
                'POTENTIELAUDITIF': POTENTIELAUDITIF,
                'RETENTISSEMENT': RETENTISSEMENT,
                'regions': regions,
                'error': error,
                'villes': villes,
                'errorValue': errorValue,

                'nom': patient.nomPatient,
                'prenom': patient.prenomPatient,
                'teleMom': patient.numTelephoneMere,
                'teleDad': patient.numTelephonePere,
                'adresse': patient.adressePatient,
                'ville': patient.villePatient,
                'delegation': patient.delegationPatient,
                'datenaissance': patient.dateNaissancePatient.strftime('%Y-%m-%d'),
                'couvertureMedicale': patient.couvertureMedical,
                'mailPatient': patient.mailPatient,
                'sexe': patient.sexePatient,
                'nomCouvertureMedical': patient.nomCouvertureMedical,
                'imgPatient': patient.imgPatient,

                'parents_Consanguins': patientInfo.parents_Consanguins,
                'age_maternel_accouchement': patientInfo.age_maternel_accouchement,
                'grossesse_suivi': patientInfo.grossesse_suivi,
                'terme_grossesse': patientInfo.terme_grossesse,
                'precisionTerme': patientInfo.precisionTerme,
                'accouchement_par_voie': patientInfo.accouchement_par_voie,
                'souffrance_neonatal': patientInfo.souffrance_neonatal,
                'poids_de_naissance': patientInfo.poids_de_naissance,
                'taille_de_naissance': patientInfo.taille_de_naissance,
                'Notion_hospitalisation_age_neonatal': patientInfo.Notion_hospitalisation_age_neonatal,
                'allaitement': patientInfo.allaitement,
                'diversification_alimentaire': patientInfo.diversification_alimentaire,
                'retentissement_staturo_ponderale': patientInfo.retentissement_staturo_ponderale,
                'assis_avec_appui': patientInfo.assis_avec_appui,
                'assis_sans_appui': patientInfo.assis_sans_appui,
                'marche_serpant': patientInfo.marche_serpant,
                'marche_4_pattes': patientInfo.marche_4_pattes,
                'debout_avec_appui': patientInfo.debout_avec_appui,
                'debout_sans_appui': patientInfo.debout_sans_appui,
                'parole_syllabe': patientInfo.parole_syllabe,
                'parole_mots': patientInfo.parole_mots,
                'parole_phrase': patientInfo.parole_phrase,
                'trouble_de_comportement': patientInfo.trouble_de_comportement,
                'trouble_de_concentration': patientInfo.trouble_de_concentration,
                'interaction_avec_entourage': patientInfo.interaction_avec_entourage,
                'spectre_autisme': patientInfo.spectre_autisme,
                'potentiel_evoque_auditif': patientInfo.potentiel_evoque_auditif,
                'caryotype': patientInfo.caryotype,
                'bilan_thyroidien': patientInfo.bilan_thyroidien,

                'pathologie_endocrinienne': patientInfo.pathologie_endocrinienne,
                'age_pathologie_endocrinienne': patientInfo.age_pathologie_endocrinienne,
                'diabete': patientInfo.diabete,
                'age_diabete': patientInfo.age_diabete,
                'obesite': patientInfo.obesite,
                'obesite_dates': obesite_dates,
                'obesite_poids': obesite_poids,
                'obesite_taille': obesite_taille,
                'imcs': imcs,

                'echo_coeur_fait': patientInfo.echo_coeur_fait,
                'echo_coeur_type': patientInfo.echo_coeur_type,
                'opere': patientInfo.opere,
                'opere_dates': opere_dates,
                'opere_types': opere_types,
                'commentairePCardiaque': patientInfo.commentairePCardiaque,

                'reflux_gastro_oesophagien': patientInfo.reflux_gastro_oesophagien,
                'maladie_coeliaque': patientInfo.maladie_coeliaque,
                'agedebut_maladie_coalique': patientInfo.agedebut_maladie_coalique,
                'mucoviscidose': patientInfo.mucoviscidose,

                'pathologie_ophtalmologique': patientInfo.pathologie_ophtalmologique,
                'pathologie_orl': patientInfo.pathologie_orl,
                'pathologie_osteoarticulaire': patientInfo.pathologie_osteoarticulaire,

                'pathologie_suivie_dentaire': patientInfo.pathologie_suivie_dentaire,
                'pathologie_suivie_dentaire_Commentaire': patientInfo.pathologie_suivie_dentaire_Commentaire,
                'suiviDentaireInfos': suiviDentaireInfos,

                'autre_pathologie': patientInfo.autre_pathologie,
                'traitement': patientInfo.traitement,

                'pathologie_neurologique': patientInfo.pathologie_neurologique,
                'epilepsie': patientInfo.epilepsie,
                'imagerie_faite': patientInfo.imagerie_faite,

                'hernies': patientInfo.hernies,
                'typeHernie_direction': patientInfo.typeHernie_direction,

                'Psychomotricien_type': patientInfo.Psychomotricien_type,
                'Psychomotricien_agedebut': patientInfo.Psychomotricien_agedebut,
                'Psychomotricien_frequenceensemaine': patientInfo.Psychomotricien_frequenceensemaine,
                'Psychomotricien_commentaire': patientInfo.Psychomotricien_commentaire,

                'Kinesitherapie_fonctionnelle_type': patientInfo.Kinesitherapie_fonctionnelle_type,
                'Kinesitherapie_fonctionnelle_agedebut': patientInfo.Kinesitherapie_fonctionnelle_agedebut,
                'Kinesitherapie_fonctionnelle_frequenceensemaine': patientInfo.Kinesitherapie_fonctionnelle_frequenceensemaine,
                'Kinesitherapie_fonctionnelle_commentaire': patientInfo.Kinesitherapie_fonctionnelle_commentaire,

                'Psychologue_type': patientInfo.Psychologue_type,
                'Psychologue_agedebut': patientInfo.Psychologue_agedebut,
                'Psychologue_frequenceensemaine': patientInfo.Psychologue_frequenceensemaine,
                'Psychologue_commentaire': patientInfo.Psychologue_commentaire,

                'Orthophoniste_type': patientInfo.Orthophoniste_type,
                'Orthophoniste_agedebut': patientInfo.Orthophoniste_agedebut,
                'Orthophoniste_frequenceensemaine': patientInfo.Orthophoniste_frequenceensemaine,
                'Orthophoniste_commentaire': patientInfo.Orthophoniste_commentaire,

                'Orthoptiste_type': patientInfo.Orthoptiste_type,
                'Orthoptiste_agedebut': patientInfo.Orthoptiste_agedebut,
                'Orthoptiste_frequenceensemaine': patientInfo.Orthoptiste_frequenceensemaine,
                'Orthoptiste_commentaire': patientInfo.Orthoptiste_commentaire,

                'scolarise': patientInfo.scolarise,
                'scolarise_age_de_début': patientInfo.scolarise_age_de_début,
                'scolarise_classe_préparatoire': patientInfo.scolarise_classe_préparatoire,
                'scolarise_bac_choice': patientInfo.scolarise_bac_choice,
                'scolarise_classe_secondaires_choice': patientInfo.scolarise_classe_secondaires_choice,
                'scolarise_classe_primaire_choice': patientInfo.scolarise_classe_primaire_choice,
                'activite_sportive': patientInfo.activite_sportive,
                'activite_artistique': patientInfo.activite_artistique,
                'activite_prof': patientInfo.activite_prof,
                'classe_primaires': classe_primaires,
                'classe_primaire_years': classe_primaire_years,
                'classe_secondaires': classe_secondaires,
                'classe_secondaire_years': classe_secondaire_years,
                'bac_years': bac_years,
                'bac_filieres': bac_filieres,
                'APr': APr,
                'AAr': AAr,
                'ASp': ASp,
                'patient_id': patient_id,
                'submitted': submitted,
            }

            if request.method == 'POST':
                imgPatient = request.FILES.get('imgPatient')
                # Section 1---------------------------------------------
                nom = request.POST.get('nom')
                prenom = request.POST.get('prenom')
                sexe = request.POST.get('sexe')
                nomCouvertureMedical = request.POST.get('nomCouvertureMedical')
                teleMom = request.POST.get('teleMom')
                teleDad = request.POST.get('teleDad')
                adresse = request.POST.get('adresse')
                ville = request.POST.get('ville')
                delegation = request.POST.get('delegation')
                datenaissance = request.POST.get('datenaissance')
                couvertureMedicale = request.POST.get('CM')
                mailPatient = request.POST.get('mailPatient')
                # Section 2---------------------------------------------
                parents_Consanguins = request.POST.get('parents_Consanguins')
                age_maternel_accouchement = request.POST.get('age_maternel_accouchement')
                grossesse_suivi = request.POST.get('grossesse_suivi')
                terme_grossesse = request.POST.get('terme_grossesse')
                precisionTerme = request.POST.get('precisionTerme')
                accouchement_par_voie = request.POST.get('accouchement_par_voie')
                souffrance_neonatal = request.POST.get('souffrance_neonatal')
                poids_de_naissance = request.POST.get('poids_de_naissance')
                taille_de_naissance = request.POST.get('taille_de_naissance')
                Notion_hospitalisation_age_neonatal = request.POST.get('Notion_hospitalisation_age_neonatal')
                allaitement = request.POST.get('allaitement')
                diversification_alimentaire = request.POST.get('diversification_alimentaire')
                retentissement_staturo_ponderale = request.POST.get('retentissement_staturo_ponderale')

                # Développement psychomoteur
                assis_avec_appui = request.POST.get('assis_avec_appui')
                assis_sans_appui = request.POST.get('assis_sans_appui')
                marche_serpant = request.POST.get('marche_serpant')
                marche_4_pattes = request.POST.get('marche_4_pattes')
                debout_avec_appui = request.POST.get('debout_avec_appui')
                debout_sans_appui = request.POST.get('debout_sans_appui')
                parole_syllabe = request.POST.get('parole_syllabe')
                parole_mots = request.POST.get('parole_mots')
                parole_phrase = request.POST.get('parole_phrase')
                trouble_de_comportement = request.POST.get('trouble_de_comportement')
                trouble_de_concentration = request.POST.get('trouble_de_concentration')
                interaction_avec_entourage = request.POST.get('interaction_avec_entourage')
                spectre_autisme = request.POST.get('spectre_autisme')
                potentiel_evoque_auditif = request.POST.get('potentiel_evoque_auditif')
                caryotype = request.POST.get('caryotype')
                bilan_thyroidien = request.POST.get('bilan_thyroidien')

                # Pathologie endocrinienne
                pathologie_endocrinienne = request.POST.get('pathologie_endocrinienne')
                age_pathologie_endocrinienne = request.POST.get('age_pathologie_endocrinienne')
                diabete = request.POST.get('diabete')
                age_diabete = request.POST.get('age_diabete')
                obesite = request.POST.get('obesite')
                obesite_dates1 = request.POST.getlist('obesite_date[]')
                obesite_poids1 = request.POST.getlist('obesite_poids[]')  # kg
                obesite_taille1 = request.POST.getlist('obesite_taille[]')  # cm (1/100 pour m)

                # Pathologie cardiaque
                echo_coeur_fait = request.POST.get('echo_coeur_fait')
                echo_coeur_type = request.POST.get('echo_coeur_type')
                opere = request.POST.get('opere')
                commentairePCardiaque = request.POST.get('commentairePCardiaque')
                opere_dates1 = request.POST.getlist('opere_date[]')
                opere_types1 = request.POST.getlist('opere_type[]')
                opere_suivi1 = request.POST.getlist('opere_suiviO[]')
                opere_suivi_date1 = request.POST.getlist('opere_suivi_date[]')

                # Pathologie digestif
                reflux_gastro_oesophagien = request.POST.get('reflux_gastro_oesophagien')
                maladie_coeliaque = request.POST.get('maladie_coeliaque')
                agedebut_maladie_coalique = request.POST.get('agedebut_maladie_coalique')
                mucoviscidose = request.POST.get('mucoviscidose')

                # Pathologie ophtalmologique
                pathologie_ophtalmologique = request.POST.get('pathologie_ophtalmologique')

                # Pathologie ORL
                pathologie_orl = request.POST.get('pathologie_orl')

                # Pathologie suivi dentaire
                pathologie_suivie_dentaire = request.POST.get('pathologie_suivie_dentaire')
                pathologie_suivie_dentaire_Commentaire = request.POST.get('pathologie_suivie_dentaire_Commentaire')
                dates_acts1 = request.POST.getlist('dates_acts[]')
                dent_GaucheDroit1 = request.POST.getlist('dent_GaucheDroit[]')
                dent_HautBas1 = request.POST.getlist('dent_HautBas[]')
                dent_num1 = request.POST.getlist('dent_num[]')
                codes_acts1 = request.POST.getlist('codes_acts[]')

                # Pathologie osteoarticulaire
                pathologie_osteoarticulaire = request.POST.get('pathologie_osteoarticulaire')

                # Pathologie neurologique
                pathologie_neurologique = request.POST.get('pathologie_neurologique')
                epilepsie = request.POST.get('epilepsie')
                imagerie_faite = request.POST.get('imagerie_faite')

                # Autre Pathologie
                autre_pathologie = request.POST.get('autre_pathologie')
                traitement = request.POST.get('traitement')

                # Hernies
                hernies = request.POST.get('hernies')
                typeHernie_direction = request.POST.get('typeHernie_direction')

                # Suivi paraclinique : Psychomotricien
                Psychomotricien_type = request.POST.get('Psychomotricien_type')
                Psychomotricien_agedebut = request.POST.get('Psychomotricien_agedebut')
                Psychomotricien_frequenceensemaine = request.POST.get('Psychomotricien_frequenceensemaine')
                Psychomotricien_commentaire = request.POST.get('Psychomotricien_commentaire')

                # Suivi paraclinique : Kinésithérapie fonctionnelle
                Kinesitherapie_fonctionnelle_type = request.POST.get('Kinesitherapie_fonctionnelle_type')
                Kinesitherapie_fonctionnelle_agedebut = request.POST.get('Kinesitherapie_fonctionnelle_agedebut')
                Kinesitherapie_fonctionnelle_frequenceensemaine = request.POST.get(
                    'Kinesitherapie_fonctionnelle_frequenceensemaine')
                Kinesitherapie_fonctionnelle_commentaire = request.POST.get('Kinesitherapie_fonctionnelle_commentaire')

                # Suivi paraclinique : Psychologue
                Psychologue_type = request.POST.get('Psychologue_type')
                Psychologue_agedebut = request.POST.get('Psychologue_agedebut')
                Psychologue_frequenceensemaine = request.POST.get('Psychologue_frequenceensemaine')
                Psychologue_commentaire = request.POST.get('Psychologue_commentaire')

                # Suivi paraclinique : Orthophoniste
                Orthophoniste_type = request.POST.get('Orthophoniste_type')
                Orthophoniste_agedebut = request.POST.get('Orthophoniste_agedebut')
                Orthophoniste_frequenceensemaine = request.POST.get('Orthophoniste_frequenceensemaine')
                Orthophoniste_commentaire = request.POST.get('Orthophoniste_commentaire')

                # Suivi paraclinique : Orthoptiste
                Orthoptiste_type = request.POST.get('Orthoptiste_type')
                Orthoptiste_agedebut = request.POST.get('Orthoptiste_agedebut')
                Orthoptiste_frequenceensemaine = request.POST.get('Orthoptiste_frequenceensemaine')
                Orthoptiste_commentaire = request.POST.get('Orthoptiste_commentaire')

                # Scolarité et activités
                scolarise = request.POST.get('scolarise')
                scolarise_age_de_début = request.POST.get('scolarise_age_de_debut')
                classe_primaires1 = request.POST.getlist('classe_primaire[]')
                scolarise_classe_préparatoire = request.POST.get('scolarise_classe_préparatoire')
                classe_primaire_years1 = request.POST.getlist('classe_primaire_year[]')
                classe_secondaires1 = request.POST.getlist('classe_secondaires[]')
                classe_secondaire_years1 = request.POST.getlist('classe_secondaires_years[]')
                bac_years1 = request.POST.getlist('BAC[]')
                bac_filieres1 = request.POST.getlist('filiere[]')
                scolarise_bac_choice = request.POST.get('bac_choice')
                scolarise_classe_secondaires_choice = request.POST.get('classe_secondaires_choice')
                scolarise_classe_primaire_choice = request.POST.get('classe_primaire_choice')
                activite_sportive = request.POST.get('activite_sportive')
                activite_artistique = request.POST.get('activite_artistique')
                activite_prof = request.POST.get('activite_prof')
                APr1 = request.POST.getlist('APr[]')
                AAr1 = request.POST.getlist('AAr[]')
                ASp1 = request.POST.getlist('ASp[]')

                # Get user
                patient = Patient.objects.get(idPatient=patient_id)
                userPatient = User.objects.get(username=patient_id)
                patientInfo = InfoPatient.objects.get(patient=patient)
                patientCardiaqueOpere = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
                patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
                patientActivite = PatientActivite.objects.filter(patientID=patient_id)
                patientScolarite = PatientScolarite.objects.filter(patientID=patient_id)
                patientDentaire = PathologieDentaire.objects.filter(patientID=patient_id)


                # Modifier User et patient
                userPatient.email = mailPatient
                userPatient.first_name = prenom
                userPatient.last_name = nom

                patient.delegationPatient = delegation
                patient.nomPatient = nom
                patient.prenomPatient = prenom
                patient.mailPatient = mailPatient
                patient.couvertureMedical = couvertureMedicale
                patient.dateNaissancePatient = datenaissance
                patient.adressePatient = adresse
                patient.numTelephoneMere = teleMom
                patient.numTelephonePere = teleDad
                patient.villePatient = ville
                patient.sexePatient = sexe
                patient.nomCouvertureMedical = nomCouvertureMedical

                if imgPatient is not None:
                    fs = FileSystemStorage(location='Uploads/imgProfile_patient/')
                    image_extention = os.path.splitext(imgPatient.name)[1][1:].lower()
                    imgPatientName = fs.save(f'{patient_id}.{image_extention}', imgPatient)
                    imgPatientAdresse = '/' + imgPatientName
                    patient.imgPatient = imgPatientAdresse

                if couvertureMedicale == "NonMutualiste":
                    nomCouvertureMedical_vide = " "
                    patient.nomCouvertureMedical = nomCouvertureMedical_vide

                patient.save()

                if scolarise != ("Oui"):
                    scolarise_classe_secondaires_choice = ""
                    scolarise_classe_primaire_choice = ""
                    scolarise_bac_choice = ""

                # Modifier patientInfo
                InfoPatient.objects.filter(patient=patient).update(patient=patient,
                                                                   parents_Consanguins=parents_Consanguins,
                                                                   age_maternel_accouchement=age_maternel_accouchement,
                                                                   grossesse_suivi=grossesse_suivi,
                                                                   terme_grossesse=terme_grossesse,
                                                                   precisionTerme=precisionTerme,
                                                                   accouchement_par_voie=accouchement_par_voie,
                                                                   souffrance_neonatal=souffrance_neonatal,
                                                                   poids_de_naissance=poids_de_naissance,
                                                                   taille_de_naissance=taille_de_naissance,
                                                                   Notion_hospitalisation_age_neonatal=Notion_hospitalisation_age_neonatal,
                                                                   allaitement=allaitement,
                                                                   diversification_alimentaire=diversification_alimentaire,
                                                                   retentissement_staturo_ponderale=retentissement_staturo_ponderale,
                                                                   assis_avec_appui=assis_avec_appui,
                                                                   assis_sans_appui=assis_sans_appui,
                                                                   marche_serpant=marche_serpant,
                                                                   marche_4_pattes=marche_4_pattes,
                                                                   debout_sans_appui=debout_sans_appui,
                                                                   debout_avec_appui=debout_avec_appui,
                                                                   parole_syllabe=parole_syllabe,
                                                                   parole_mots=parole_mots,
                                                                   parole_phrase=parole_phrase,
                                                                   interaction_avec_entourage=interaction_avec_entourage,
                                                                   trouble_de_concentration=trouble_de_concentration,
                                                                   trouble_de_comportement=trouble_de_comportement,
                                                                   spectre_autisme=spectre_autisme,
                                                                   caryotype=caryotype,
                                                                   potentiel_evoque_auditif=potentiel_evoque_auditif,
                                                                   bilan_thyroidien=bilan_thyroidien,

                                                                   pathologie_endocrinienne=pathologie_endocrinienne,
                                                                   age_pathologie_endocrinienne=age_pathologie_endocrinienne,
                                                                   diabete=diabete,
                                                                   age_diabete=age_diabete,
                                                                   obesite=obesite,

                                                                   echo_coeur_fait=echo_coeur_fait,
                                                                   echo_coeur_type=echo_coeur_type,
                                                                   opere=opere,
                                                                   commentairePCardiaque=commentairePCardiaque,

                                                                   reflux_gastro_oesophagien=reflux_gastro_oesophagien,
                                                                   maladie_coeliaque=maladie_coeliaque,
                                                                   agedebut_maladie_coalique=agedebut_maladie_coalique,
                                                                   mucoviscidose=mucoviscidose,

                                                                   hernies=hernies,
                                                                   typeHernie_direction=typeHernie_direction,

                                                                   pathologie_ophtalmologique=pathologie_ophtalmologique,
                                                                   pathologie_orl=pathologie_orl,
                                                                   pathologie_osteoarticulaire=pathologie_osteoarticulaire,

                                                                   pathologie_suivie_dentaire_Commentaire=pathologie_suivie_dentaire_Commentaire,
                                                                   pathologie_suivie_dentaire=pathologie_suivie_dentaire,

                                                                   pathologie_neurologique=pathologie_neurologique,
                                                                   epilepsie=epilepsie,
                                                                   imagerie_faite=imagerie_faite,

                                                                   traitement=traitement,
                                                                   autre_pathologie=autre_pathologie,

                                                                   Psychologue_type=Psychologue_type,
                                                                   Psychologue_agedebut=Psychologue_agedebut,
                                                                   Psychologue_frequenceensemaine=Psychologue_frequenceensemaine,
                                                                   Psychologue_commentaire=Psychologue_commentaire,

                                                                   Orthophoniste_type=Orthophoniste_type,
                                                                   Orthophoniste_agedebut=Orthophoniste_agedebut,
                                                                   Orthophoniste_frequenceensemaine=Orthophoniste_frequenceensemaine,
                                                                   Orthophoniste_commentaire=Orthophoniste_commentaire,

                                                                   Psychomotricien_type=Psychomotricien_type,
                                                                   Psychomotricien_agedebut=Psychomotricien_agedebut,
                                                                   Psychomotricien_frequenceensemaine=Psychomotricien_frequenceensemaine,
                                                                   Psychomotricien_commentaire=Psychomotricien_commentaire,

                                                                   Kinesitherapie_fonctionnelle_type=Kinesitherapie_fonctionnelle_type,
                                                                   Kinesitherapie_fonctionnelle_agedebut=Kinesitherapie_fonctionnelle_agedebut,
                                                                   Kinesitherapie_fonctionnelle_frequenceensemaine=Kinesitherapie_fonctionnelle_frequenceensemaine,
                                                                   Kinesitherapie_fonctionnelle_commentaire=Kinesitherapie_fonctionnelle_commentaire,

                                                                   Orthoptiste_type=Orthoptiste_type,
                                                                   Orthoptiste_agedebut=Orthoptiste_agedebut,
                                                                   Orthoptiste_frequenceensemaine=Orthoptiste_frequenceensemaine,
                                                                   Orthoptiste_commentaire=Orthoptiste_commentaire,

                                                                   scolarise=scolarise,
                                                                   scolarise_age_de_début=scolarise_age_de_début,
                                                                   scolarise_classe_préparatoire=scolarise_classe_préparatoire,
                                                                   scolarise_bac_choice=scolarise_bac_choice,
                                                                   scolarise_classe_secondaires_choice=scolarise_classe_secondaires_choice,
                                                                   scolarise_classe_primaire_choice=scolarise_classe_primaire_choice,
                                                                   activite_sportive=activite_sportive,
                                                                   activite_artistique=activite_artistique,
                                                                   activite_prof=activite_prof)
                patientCardiaqueOpere.delete()
                patientObeseteImc.delete()
                patientActivite.delete()
                patientScolarite.delete()
                patientDentaire.delete()

                if pathologie_suivie_dentaire == ("Oui"):
                    for x in range(0, len(dates_acts1)):
                        pathologieDentaire = PathologieDentaire(patientID=patient_id,
                                                                date_act=dates_acts1[x],
                                                                dent_GaucheDroit=dent_GaucheDroit1[x],
                                                                dent_HautBas=dent_HautBas1[x],
                                                                dent_num=dent_num1[x],
                                                                code_act=codes_acts1[x], )
                        pathologieDentaire.save()

                if opere == ("Oui"):
                    osd = 0
                    for x in range(0, len(opere_dates1)):
                        patientOpere = PathologieCardiqueOpere(patientID=patient_id,
                                                               opere_date=opere_dates1[x],
                                                               opere_type=opere_types1[x],
                                                               opere_suivi = opere_suivi1[x],)
                        patientOpere.save()
                        if patientOpere.opere_suivi == "Oui":
                            patientOpere.opere_suivi_date=opere_suivi_date1[osd]
                            osd = osd + 1
                            patientOpere.save()

                if obesite == ("Oui"):
                    for x in range(0, len(obesite_dates1)):
                        patientObesite = ObesiteImc(patientID=patient_id,
                                                    obesite_date=obesite_dates1[x],
                                                    obesite_poids=obesite_poids1[x],
                                                    obesite_taille=obesite_taille1[x],
                                                    imc=round(float(obesite_poids1[x]) / ((float(obesite_taille1[x]) / 100) ** 2), 3))
                        patientObesite.save()
                if (activite_prof == ("Oui")):
                    for x in APr1:
                        patientActivite = PatientActivite(patientID=patient_id,
                                                          type_activite="Activite professionnel",
                                                          description_activite=x)
                        patientActivite.save()
                if (activite_artistique == ("Oui")):
                    for x in AAr1:
                        patientActivite = PatientActivite(patientID=patient_id,
                                                          type_activite="Activite artistique",
                                                          description_activite=x)
                        patientActivite.save()
                if (activite_sportive == ("Oui")):
                    for x in ASp1:
                        patientActivite = PatientActivite(patientID=patient_id,
                                                          type_activite="Activite sportive",
                                                          description_activite=x)
                        patientActivite.save()
                if scolarise == ("Oui"):
                    if scolarise_classe_primaire_choice == ("on"):
                        for x in range(0, len(classe_primaires1)):
                            patientScolaritePrimaire = PatientScolarite(patientID=patient_id,
                                                                        type_scolarite="Classe primaire",
                                                                        level_scolarite=classe_primaires1[x],
                                                                        year_scolarite=classe_primaire_years1[x])
                            patientScolaritePrimaire.save()
                    if scolarise_classe_secondaires_choice == ("on"):
                        for x in range(0, len(classe_secondaires1)):
                            patientScolariteSecondaire = PatientScolarite(patientID=patient_id,
                                                                          type_scolarite="Classe secondaire",
                                                                          level_scolarite=classe_secondaires1[x],
                                                                          year_scolarite=classe_secondaire_years1[x])
                            patientScolariteSecondaire.save()
                    if scolarise_bac_choice == ("on"):
                        for x in range(0, len(bac_filieres1)):
                            patientScolariteBac = PatientScolarite(patientID=patient_id,
                                                                   type_scolarite="BAC",
                                                                   level_scolarite=bac_filieres1[x],
                                                                   year_scolarite=bac_years1[x])
                            patientScolariteBac.save()

                """
                                try:

                                except BaseException as e:
                                    errorMessage = str(e)
                                    errorValue = True
                                    url = reverse('home_pediatre') + f'?error={errorMessage}&errorValue={errorValue}'
                                    return redirect(url)
                                
                else:
                    return redirect('afficher_infos_patient', patient_id=patient_id)
                """
                return redirect('afficher_infos_patient', patient_id=patient_id)
            else:
                if 'submitted' in request.GET:
                    submitted = True
            return render(request, 'Pediatre/modifierPatient_pediatre.html', context)
    else:
        return redirect('login_pediatre')


def supprimer_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        patients = []
        try:
            # Delete User Automaticly delete the patient and InfoPatient
            userPatient = User.objects.get(username=patient_id)
            userPatient.delete()

            # Delete other Informations
            patientActivite = PatientActivite.objects.filter(patientID=patient_id)
            patientActivite.delete()
            patientScolarite = PatientScolarite.objects.filter(patientID=patient_id)
            patientScolarite.delete()
            patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
            patientOpereCardiaque.delete()
            patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
            patientObeseteImc.delete()
            patientDentaire = PathologieDentaire.objects.filter(patientID=patient_id)
            patientDentaire.delete()

            # Delete patient
            # patient = Patient.objects.get(idPatient=patient_id, is_deleted="Oui")
            # patientInfo = InfoPatient.objects.get(patient=patient)
            # patientInfo.delete()
            # patient.delete()

            # Redirect
            return redirect('corbeille_patient')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            url = reverse('home_pediatre') + f'?error={errorMessage}&errorValue={errorValue}'
            return redirect(url)
    else:
        return redirect('login_pediatre')


def pediatre(request):
    return render(request, 'Pediatre/pediatre.html')


def recherche_patient(request):
    if request.user.is_authenticated:
        submitted = False
        error = ""
        errorValue = False
        patients = []

        if request.method == 'POST':
            IdPatient_recherche = request.POST.get('IdPatient_recherche')
            nomPatient_recherche = request.POST.get('nomPatient_recherche')
            prenomPatient_recherche = request.POST.get('prenomPatient_recherche')
            dateNPatient_recherche = request.POST.get('dateNPatient_recherche')
            regionPatient_recherche = request.POST.get('regionPatient_recherche')

            if (IdPatient_recherche != ""):
                try:
                    pediatre = Pediatre.objects.get(user=request.user)
                    patients_id = Patient.objects.filter(inpe=pediatre, idPatient__icontains=IdPatient_recherche,
                                                         is_deleted="Non")
                except BaseException as e:
                    print("Caught exception:", e)
                    error = str(e)
                    errorValue = True
                else:
                    if (nomPatient_recherche != ""):
                        try:
                            patients_id_nom = patients_id.filter(nomPatient__icontains=nomPatient_recherche)
                        except BaseException as e:
                            print("Caught exception:", e)
                            error = str(e)
                            errorValue = True
                        else:
                            if (prenomPatient_recherche != ""):
                                try:
                                    patients_id_nom_prenom = patients_id_nom.filter(
                                        prenomPatient__icontains=prenomPatient_recherche)
                                except BaseException as e:
                                    print("Caught exception:", e)
                                    error = str(e)
                                    errorValue = True
                                else:
                                    if (dateNPatient_recherche != ""):
                                        try:
                                            patients_id_nom_prenom_dn = patients_id_nom_prenom.filter(
                                                dateNaissancePatient=dateNPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            if (regionPatient_recherche != ""):
                                                try:
                                                    patients_id_nom_prenom_dn_mail = patients_id_nom_prenom_dn.filter(
                                                        delegationPatient__icontains=regionPatient_recherche)
                                                except BaseException as e:
                                                    print("Caught exception:", e)
                                                    error = str(e)
                                                    errorValue = True
                                                else:
                                                    context = {
                                                        'error': error,
                                                        'errorValue': errorValue,
                                                        'patients': patients_id_nom_prenom_dn_mail,
                                                    }
                                                    return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                                  context)
                                            else:
                                                context = {
                                                    'error': error,
                                                    'errorValue': errorValue,
                                                    'patients': patients_id_nom_prenom_dn,
                                                }
                                                return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                              context)
                                    else:
                                        if (regionPatient_recherche != ""):
                                            try:
                                                patients_id_nom_prenom_mail = patients_id_nom_prenom.filter(
                                                    delegationPatient__icontains=regionPatient_recherche)
                                            except BaseException as e:
                                                print("Caught exception:", e)
                                                error = str(e)
                                                errorValue = True
                                            else:
                                                context = {
                                                    'error': error,
                                                    'errorValue': errorValue,
                                                    'patients': patients_id_nom_prenom_mail,
                                                }
                                                return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                              context)
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_nom_prenom,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)

                            else:
                                if (dateNPatient_recherche != ""):
                                    try:
                                        patients_id_nom_dn = patients_id_nom.filter(
                                            dateNaissancePatient=dateNPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        if (regionPatient_recherche != ""):
                                            try:
                                                patients_id_nom_dn_mail = patients_id_nom_dn.filter(
                                                    delegationPatient__icontains=regionPatient_recherche)
                                            except BaseException as e:
                                                print("Caught exception:", e)
                                                error = str(e)
                                                errorValue = True
                                            else:
                                                context = {
                                                    'error': error,
                                                    'errorValue': errorValue,
                                                    'patients': patients_id_nom_dn_mail,
                                                }
                                                return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                              context)
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_nom_dn,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_id_nom_mail = patients_id_nom.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_nom_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_id_nom,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)

                    else:
                        if (prenomPatient_recherche != ""):
                            try:
                                patients_id_prenom = patients_id.filter(
                                    prenomPatient__icontains=prenomPatient_recherche)
                            except BaseException as e:
                                print("Caught exception:", e)
                                error = str(e)
                                errorValue = True
                            else:
                                if (dateNPatient_recherche != ""):
                                    try:
                                        patients_id_prenom_dn = patients_id_prenom.filter(
                                            dateNaissancePatient=dateNPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        if (regionPatient_recherche != ""):
                                            try:
                                                patients_id_prenom_dn_mail = patients_id_prenom_dn.filter(
                                                    delegationPatient__icontains=regionPatient_recherche)
                                            except BaseException as e:
                                                print("Caught exception:", e)
                                                error = str(e)
                                                errorValue = True
                                            else:
                                                context = {
                                                    'error': error,
                                                    'errorValue': errorValue,
                                                    'patients': patients_id_prenom_dn_mail,
                                                }
                                                return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                              context)
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_prenom_dn,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_id_prenom_mail = patients_id_prenom.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_prenom_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_id_prenom,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)

                        else:
                            if (dateNPatient_recherche != ""):
                                try:
                                    patients_id_dn = patients_id.filter(
                                        dateNaissancePatient=dateNPatient_recherche)
                                except BaseException as e:
                                    print("Caught exception:", e)
                                    error = str(e)
                                    errorValue = True
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_id_dn_mail = patients_id_dn.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_id_dn_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_id_dn,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                            else:
                                if (regionPatient_recherche != ""):
                                    try:
                                        patients_id_mail = patients_id.filter(
                                            delegationPatient__icontains=regionPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_id_mail,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    context = {
                                        'error': error,
                                        'errorValue': errorValue,
                                        'patients': patients_id,
                                    }
                                    return render(request, 'Pediatre/recherchePatients_pediatre.html', context)

            else:
                if (nomPatient_recherche != ""):
                    try:
                        pediatre = Pediatre.objects.get(user=request.user)
                        patients_nom = Patient.objects.filter(inpe=pediatre, nomPatient__icontains=nomPatient_recherche,
                                                              is_deleted="Non")
                    except BaseException as e:
                        print("Caught exception:", e)
                        error = str(e)
                        errorValue = True
                    else:
                        if (prenomPatient_recherche != ""):
                            try:
                                patients_nom_prenom = patients_nom.filter(
                                    prenomPatient__icontains=prenomPatient_recherche)
                            except BaseException as e:
                                print("Caught exception:", e)
                                error = str(e)
                                errorValue = True
                            else:
                                if (dateNPatient_recherche != ""):
                                    try:
                                        patients_nom_prenom_dn = patients_nom_prenom.filter(
                                            dateNaissancePatient=dateNPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        if (regionPatient_recherche != ""):
                                            try:
                                                patients_nom_prenom_dn_mail = patients_nom_prenom_dn.filter(
                                                    delegationPatient__icontains=regionPatient_recherche)
                                            except BaseException as e:
                                                print("Caught exception:", e)
                                                error = str(e)
                                                errorValue = True
                                            else:
                                                context = {
                                                    'error': error,
                                                    'errorValue': errorValue,
                                                    'patients': patients_nom_prenom_dn_mail,
                                                }
                                                return render(request, 'Pediatre/recherchePatients_pediatre.html',
                                                              context)
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_nom_prenom_dn,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_nom_prenom_mail = patients_nom_prenom.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_nom_prenom_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_nom_prenom,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                        else:
                            if (dateNPatient_recherche != ""):
                                try:
                                    patients_nom_dn = patients_nom.filter(
                                        dateNaissancePatient=dateNPatient_recherche)
                                except BaseException as e:
                                    print("Caught exception:", e)
                                    error = str(e)
                                    errorValue = True
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_nom_dn_mail = patients_nom_dn.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_nom_dn_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_nom_dn,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                            else:
                                if (regionPatient_recherche != ""):
                                    try:
                                        patients_nom_mail = patients_nom.filter(
                                            delegationPatient__icontains=regionPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_nom_mail,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    context = {
                                        'error': error,
                                        'errorValue': errorValue,
                                        'patients': patients_nom,
                                    }
                                    return render(request, 'Pediatre/recherchePatients_pediatre.html', context)

                else:
                    if (prenomPatient_recherche != ""):
                        try:
                            pediatre = Pediatre.objects.get(user=request.user)
                            patients_prenom = Patient.objects.filter(inpe=pediatre,
                                                                     prenomPatient__icontains=prenomPatient_recherche,
                                                                     is_deleted="Non")
                        except BaseException as e:
                            print("Caught exception:", e)
                            error = str(e)
                            errorValue = True
                        else:
                            if (dateNPatient_recherche != ""):
                                try:
                                    patients_prenom_dn = patients_prenom.filter(
                                        dateNaissancePatient=dateNPatient_recherche)
                                except BaseException as e:
                                    print("Caught exception:", e)
                                    error = str(e)
                                    errorValue = True
                                else:
                                    if (regionPatient_recherche != ""):
                                        try:
                                            patients_prenom_dn_mail = patients_prenom_dn.filter(
                                                delegationPatient__icontains=regionPatient_recherche)
                                        except BaseException as e:
                                            print("Caught exception:", e)
                                            error = str(e)
                                            errorValue = True
                                        else:
                                            context = {
                                                'error': error,
                                                'errorValue': errorValue,
                                                'patients': patients_prenom_dn_mail,
                                            }
                                            return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_prenom_dn,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                            else:
                                if (regionPatient_recherche != ""):
                                    try:
                                        patients_prenom_mail = patients_prenom.filter(
                                            delegationPatient__icontains=regionPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_prenom_mail,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    context = {
                                        'error': error,
                                        'errorValue': errorValue,
                                        'patients': patients_prenom,
                                    }
                                    return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                    else:
                        if (dateNPatient_recherche != ""):
                            try:
                                pediatre = Pediatre.objects.get(user=request.user)
                                patients_dn = Patient.objects.filter(inpe=pediatre,
                                                                     dateNaissancePatient=dateNPatient_recherche,
                                                                     is_deleted="Non")
                            except BaseException as e:
                                print("Caught exception:", e)
                                error = str(e)
                                errorValue = True
                            else:
                                if (regionPatient_recherche != ""):
                                    try:
                                        patients_dn_mail = patients_dn.filter(
                                            delegationPatient__icontains=regionPatient_recherche)
                                    except BaseException as e:
                                        print("Caught exception:", e)
                                        error = str(e)
                                        errorValue = True
                                    else:
                                        context = {
                                            'error': error,
                                            'errorValue': errorValue,
                                            'patients': patients_dn_mail,
                                        }
                                        return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                                else:
                                    context = {
                                        'error': error,
                                        'errorValue': errorValue,
                                        'patients': patients_dn,
                                    }
                                    return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                        else:
                            if (regionPatient_recherche != ""):
                                try:
                                    pediatre = Pediatre.objects.get(user=request.user)
                                    patients_mail = Patient.objects.filter(inpe=pediatre,
                                                                           delegationPatient__icontains=regionPatient_recherche,
                                                                           is_deleted="Non")
                                except BaseException as e:
                                    print("Caught exception:", e)
                                    error = str(e)
                                    errorValue = True
                                else:
                                    context = {
                                        'error': error,
                                        'errorValue': errorValue,
                                        'patients': patients_mail,
                                    }
                                    return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
                            else:
                                context = {
                                    'error': error,
                                    'errorValue': errorValue,
                                    'patients': patients,
                                }
                                return render(request, 'Pediatre/recherchePatients_pediatre.html', context)
        else:
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'Pediatre/recherchePatients_pediatre.html',
                      {'error': error, 'errorValue': errorValue, 'submitted': submitted,
                       'patients': patients, })
    else:
        return redirect('login_pediatre')


def afficher_infos_patient(request, patient_id):
    if request.user.is_authenticated:
        errorMessage = ""
        errorValue = False
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            # Retrieve the user data
            obesite_dates_user = ObesiteImc.objects.filter(patientID=patient_id).values_list('obesite_date', flat=True)
            obesite_poids_user = ObesiteImc.objects.filter(patientID=patient_id).values_list('obesite_poids', flat=True)
            obesite_taille_user = ObesiteImc.objects.filter(patientID=patient_id).values_list('obesite_taille', flat=True)
            obesite_imc_user = ObesiteImc.objects.filter(patientID=patient_id).values_list('imc', flat=True)

        except ObjectDoesNotExist:
            errorMessage = "Impossible de trouver un patient avec l'ID " + str(patient_id)
            errorValue = True
            url = reverse('home_pediatre') + f'?error={errorMessage}&errorValue={errorValue}'
            return redirect(url)
        else:
            try:
                patientInfo = InfoPatient.objects.get(patient=patient)
            except ObjectDoesNotExist:
                errorMessage = "Impossible de trouver les informations sur le patient avec l'ID " + str(patient_id)
                errorValue = True
                url = reverse('home_pediatre') + f'?error={errorMessage}&errorValue={errorValue}'
                return redirect(url)
            else:
                # Declaration des vars
                classe_primaires = []
                classe_primaire_years = []
                classe_secondaires = []
                classe_secondaire_years = []
                bac_years = []
                bac_filieres = []
                ASp = []
                APr = []
                AAr = []
                opere_dates = []
                opere_types = []
                opere_suivis = []
                opere_suivi_dates = []
                obesite_dates = []
                obesite_poids = []
                obesite_taille = []
                imcs = []
                data_poids = []
                data_taille = []
                data_imc = []
                age_list = []
                dates_acts = []
                dent_GaucheDroits = []
                dent_HautBass = []
                dent_nums = []
                codes_acts = []

                if patientInfo.pathologie_suivie_dentaire == "Oui":
                    patientDentaire = PathologieDentaire.objects.filter(patientID=patient_id)
                    for x in patientDentaire:
                        dates_acts.append(x.date_act)
                        dent_GaucheDroits.append(x.dent_GaucheDroit)
                        dent_HautBass.append(x.dent_HautBas)
                        dent_nums.append(x.dent_num)
                        codes_acts.append(x.code_act)

                if (patientInfo.opere == "Oui"):
                    patientOpereCardiaque = PathologieCardiqueOpere.objects.filter(patientID=patient_id)
                    for x in patientOpereCardiaque:
                        opere_dates.append(x.opere_date)
                        opere_types.append(x.opere_type)
                        opere_suivis.append(x.opere_suivi)
                        opere_suivi_dates.append(x.opere_suivi_date)

                if (patientInfo.obesite == "Oui"):
                    patientObeseteImc = ObesiteImc.objects.filter(patientID=patient_id)
                    for x in patientObeseteImc:
                        obesite_dates.append(x.obesite_date)
                        obesite_poids.append(x.obesite_poids)
                        obesite_taille.append(x.obesite_taille)
                        imcs.append(x.imc)

                if (patientInfo.scolarise == "Oui"):
                    # classe_primaire_years classe_primaires
                    if patientInfo.scolarise_classe_primaire_choice == "on":
                        patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                           type_scolarite="Classe primaire")
                        for x in patientScolarite:
                            classe_primaires.append(x.level_scolarite)
                            classe_primaire_years.append(x.year_scolarite)

                    # "Classe secondaire" classe_secondaire_years classe_secondaires
                    if patientInfo.scolarise_classe_secondaires_choice == "on":
                        patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                           type_scolarite="Classe secondaire")
                        for x in patientScolarite:
                            classe_secondaires.append(x.level_scolarite)
                            classe_secondaire_years.append(x.year_scolarite)

                    # ""BAC"" bac_years bac_filieres
                    if patientInfo.scolarise_bac_choice == "on":
                        patientScolarite = PatientScolarite.objects.filter(patientID=patient_id,
                                                                           type_scolarite="BAC")
                        for x in patientScolarite:
                            bac_filieres.append(x.level_scolarite)
                            bac_years.append(x.year_scolarite)

                if (patientInfo.activite_sportive == "Oui"):
                    patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                     type_activite="Activite sportive")
                    for x in patientActivite:
                        ASp.append(x.description_activite)

                if (patientInfo.activite_artistique == "Oui"):
                    patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                     type_activite="Activite artistique")
                    for x in patientActivite:
                        AAr.append(x.description_activite)

                if (patientInfo.activite_prof == "Oui"):
                    patientActivite = PatientActivite.objects.filter(patientID=patient_id,
                                                                     type_activite="Activite professionnel")
                    for x in patientActivite:
                        APr.append(x.description_activite)

                #Statics Code
                birthday = patient.dateNaissancePatient
                for obesite_date in obesite_dates_user:
                    age_delta = relativedelta(obesite_date, birthday)
                    age = age_delta.years + age_delta.months / 12 + age_delta.days / 365
                    age_list.append(age)

                for i in range(0, len(age_list)):
                    data_poids.append([age_list[i], obesite_poids_user[i]])
                    data_taille.append([age_list[i], obesite_taille_user[i]])
                    data_imc.append([age_list[i], obesite_imc_user[i]])

                data_json_poids = json.dumps(data_poids, cls=DjangoJSONEncoder)
                data_json_taille = json.dumps(data_taille, cls=DjangoJSONEncoder)
                data_json_imc = json.dumps(data_imc, cls=DjangoJSONEncoder)

                # Take the image URL
                file_name = os.path.basename(patient.imgPatient.url)
                img_path = "/imgProfile_patient/" + file_name

                context = {
                    'errorMessage': errorMessage,
                    'errorValue': errorValue,

                    'data_poids': data_json_poids,
                    'data_taille': data_json_taille,
                    'data_imc': data_json_imc,

                    'patient_id': patient_id,
                    'nom': patient.nomPatient,
                    'prenom': patient.prenomPatient,
                    'sexe': patient.sexePatient,
                    'nomCouvertureMedical': patient.nomCouvertureMedical,
                    'teleMom': patient.numTelephoneMere,
                    'teleDad': patient.numTelephonePere,
                    'adresse': patient.adressePatient,
                    'imgPatient': img_path,
                    'ville': patient.villePatient,
                    'delegation': patient.delegationPatient,
                    'datenaissance': patient.dateNaissancePatient,
                    'couvertureMedicale': patient.couvertureMedical,
                    'mailPatient': patient.mailPatient,

                    'parents_Consanguins': patientInfo.parents_Consanguins,
                    'age_maternel_accouchement': patientInfo.age_maternel_accouchement,
                    'grossesse_suivi': patientInfo.grossesse_suivi,
                    'terme_grossesse': patientInfo.terme_grossesse,
                    'precisionTerme': patientInfo.precisionTerme,
                    'accouchement_par_voie': patientInfo.accouchement_par_voie,
                    'souffrance_neonatal': patientInfo.souffrance_neonatal,
                    'poids_de_naissance': patientInfo.poids_de_naissance,
                    'taille_de_naissance': patientInfo.taille_de_naissance,
                    'Notion_hospitalisation_age_neonatal': patientInfo.Notion_hospitalisation_age_neonatal,
                    'allaitement': patientInfo.allaitement,
                    'diversification_alimentaire': patientInfo.diversification_alimentaire,
                    'retentissement_staturo_ponderale': patientInfo.retentissement_staturo_ponderale,
                    'assis_avec_appui': patientInfo.assis_avec_appui,
                    'assis_sans_appui': patientInfo.assis_sans_appui,
                    'marche_serpant': patientInfo.marche_serpant,
                    'marche_4_pattes': patientInfo.marche_4_pattes,
                    'debout_avec_appui': patientInfo.debout_avec_appui,
                    'debout_sans_appui': patientInfo.debout_sans_appui,
                    'parole_syllabe': patientInfo.parole_syllabe,
                    'parole_mots': patientInfo.parole_mots,
                    'parole_phrase': patientInfo.parole_phrase,
                    'trouble_de_comportement': patientInfo.trouble_de_comportement,
                    'trouble_de_concentration': patientInfo.trouble_de_concentration,
                    'interaction_avec_entourage': patientInfo.interaction_avec_entourage,
                    'spectre_autisme': patientInfo.spectre_autisme,
                    'potentiel_evoque_auditif': patientInfo.potentiel_evoque_auditif,
                    'caryotype': patientInfo.caryotype,
                    'bilan_thyroidien': patientInfo.bilan_thyroidien,

                    'pathologie_endocrinienne': patientInfo.pathologie_endocrinienne,
                    'age_pathologie_endocrinienne': patientInfo.age_pathologie_endocrinienne,
                    'diabete': patientInfo.diabete,
                    'age_diabete': patientInfo.age_diabete,
                    'obesite': patientInfo.obesite,
                    'obesite_dates': obesite_dates,
                    'obesite_poids': obesite_poids,
                    'obesite_taille': obesite_taille,
                    'imcs': imcs,

                    'echo_coeur_fait': patientInfo.echo_coeur_fait,
                    'echo_coeur_type': patientInfo.echo_coeur_type,
                    'opere': patientInfo.opere,
                    'opere_dates': opere_dates,
                    'opere_suivis': opere_suivis,
                    'opere_types': opere_types,
                    'opere_suivi_dates': opere_suivi_dates,
                    'commentairePCardiaque': patientInfo.commentairePCardiaque,

                    'reflux_gastro_oesophagien': patientInfo.reflux_gastro_oesophagien,
                    'maladie_coeliaque': patientInfo.maladie_coeliaque,
                    'agedebut_maladie_coalique': patientInfo.agedebut_maladie_coalique,
                    'mucoviscidose': patientInfo.mucoviscidose,

                    'pathologie_ophtalmologique': patientInfo.pathologie_ophtalmologique,
                    'pathologie_orl': patientInfo.pathologie_orl,
                    'pathologie_osteoarticulaire': patientInfo.pathologie_osteoarticulaire,

                    'pathologie_suivie_dentaire': patientInfo.pathologie_suivie_dentaire,
                    'pathologie_suivie_dentaire_Commentaire': patientInfo.pathologie_suivie_dentaire_Commentaire,
                    'dates_acts': dates_acts,
                    'dent_GaucheDroits': dent_GaucheDroits,
                    'dent_HautBass': dent_HautBass,
                    'dent_nums': dent_nums,
                    'codes_acts': codes_acts,

                    'autre_pathologie': patientInfo.autre_pathologie,
                    'traitement': patientInfo.traitement,

                    'pathologie_neurologique': patientInfo.pathologie_neurologique,
                    'epilepsie': patientInfo.epilepsie,
                    'imagerie_faite': patientInfo.imagerie_faite,

                    'hernies': patientInfo.hernies,
                    'typeHernie_direction': patientInfo.typeHernie_direction,

                    'Psychomotricien_type': patientInfo.Psychomotricien_type,
                    'Psychomotricien_agedebut': patientInfo.Psychomotricien_agedebut,
                    'Psychomotricien_frequenceensemaine': patientInfo.Psychomotricien_frequenceensemaine,
                    'Psychomotricien_commentaire': patientInfo.Psychomotricien_commentaire,

                    'Kinesitherapie_fonctionnelle_type': patientInfo.Kinesitherapie_fonctionnelle_type,
                    'Kinesitherapie_fonctionnelle_agedebut': patientInfo.Kinesitherapie_fonctionnelle_agedebut,
                    'Kinesitherapie_fonctionnelle_frequenceensemaine': patientInfo.Kinesitherapie_fonctionnelle_frequenceensemaine,
                    'Kinesitherapie_fonctionnelle_commentaire': patientInfo.Kinesitherapie_fonctionnelle_commentaire,

                    'Psychologue_type': patientInfo.Psychologue_type,
                    'Psychologue_agedebut': patientInfo.Psychologue_agedebut,
                    'Psychologue_frequenceensemaine': patientInfo.Psychologue_frequenceensemaine,
                    'Psychologue_commentaire': patientInfo.Psychologue_commentaire,

                    'Orthophoniste_type': patientInfo.Orthophoniste_type,
                    'Orthophoniste_agedebut': patientInfo.Orthophoniste_agedebut,
                    'Orthophoniste_frequenceensemaine': patientInfo.Orthophoniste_frequenceensemaine,
                    'Orthophoniste_commentaire': patientInfo.Orthophoniste_commentaire,

                    'Orthoptiste_type': patientInfo.Orthoptiste_type,
                    'Orthoptiste_agedebut': patientInfo.Orthoptiste_agedebut,
                    'Orthoptiste_frequenceensemaine': patientInfo.Orthoptiste_frequenceensemaine,
                    'Orthoptiste_commentaire': patientInfo.Orthoptiste_commentaire,

                    'scolarise': patientInfo.scolarise,
                    'scolarise_age_de_début': patientInfo.scolarise_age_de_début,
                    'scolarise_classe_préparatoire': patientInfo.scolarise_classe_préparatoire,
                    'scolarise_bac_choice': patientInfo.scolarise_bac_choice,
                    'scolarise_classe_secondaires_choice': patientInfo.scolarise_classe_secondaires_choice,
                    'scolarise_classe_primaire_choice': patientInfo.scolarise_classe_primaire_choice,
                    'activite_sportive': patientInfo.activite_sportive,
                    'activite_artistique': patientInfo.activite_artistique,
                    'activite_prof': patientInfo.activite_prof,

                    'classe_primaires': classe_primaires,
                    'classe_primaire_years': classe_primaire_years,
                    'classe_secondaires': classe_secondaires,
                    'classe_secondaire_years': classe_secondaire_years,
                    'bac_years': bac_years,
                    'bac_filieres': bac_filieres,
                    'APr': APr,
                    'AAr': AAr,
                    'ASp': ASp,
                }
                return render(request, 'Pediatre/afficherPatient_pediatre.html', context)
    else:
        return redirect('login_pediatre')


def ajouter_patient_pediatre(request):
    if request.user.is_authenticated:
        submitted = False
        error = ""
        errorValue = False
        if request.method == 'POST':
            imgPatient = request.FILES.get('imgPatient')
            # Section 1---------------------------------------------
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            sexe = request.POST.get('sexe')
            nomCouvertureMedical = request.POST.get('nomCouvertureMedical')
            teleMom = request.POST.get('teleMom')
            teleDad = request.POST.get('teleDad')
            adresse = request.POST.get('adresse')
            ville = request.POST.get('ville')
            delegation = request.POST.get('delegation')
            datenaissance = request.POST.get('datenaissance')
            couvertureMedicale = request.POST.get('CM')
            mailPatient = request.POST.get('mailPatient')
            # Section 2---------------------------------------------
            parents_Consanguins = request.POST.get('parents_Consanguins')
            age_maternel_accouchement = request.POST.get('age_maternel_accouchement')
            grossesse_suivi = request.POST.get('grossesse_suivi')
            terme_grossesse = request.POST.get('terme_grossesse')
            precisionTerme = request.POST.get('precisionTerme')
            accouchement_par_voie = request.POST.get('accouchement_par_voie')
            souffrance_neonatal = request.POST.get('souffrance_neonatal')
            poids_de_naissance = request.POST.get('poids_de_naissance')
            taille_de_naissance = request.POST.get('taille_de_naissance')
            Notion_hospitalisation_age_neonatal = request.POST.get('Notion_hospitalisation_age_neonatal')
            allaitement = request.POST.get('allaitement')
            diversification_alimentaire = request.POST.get('diversification_alimentaire')
            retentissement_staturo_ponderale = request.POST.get('retentissement_staturo_ponderale')

            # Développement psychomoteur
            assis_avec_appui = request.POST.get('assis_avec_appui')
            assis_sans_appui = request.POST.get('assis_sans_appui')
            marche_serpant = request.POST.get('marche_serpant')
            marche_4_pattes = request.POST.get('marche_4_pattes')
            debout_avec_appui = request.POST.get('debout_avec_appui')
            debout_sans_appui = request.POST.get('debout_sans_appui')
            parole_syllabe = request.POST.get('parole_syllabe')
            parole_mots = request.POST.get('parole_mots')
            parole_phrase = request.POST.get('parole_phrase')
            trouble_de_comportement = request.POST.get('trouble_de_comportement')
            trouble_de_concentration = request.POST.get('trouble_de_concentration')
            interaction_avec_entourage = request.POST.get('interaction_avec_entourage')
            spectre_autisme = request.POST.get('spectre_autisme')
            potentiel_evoque_auditif = request.POST.get('potentiel_evoque_auditif')
            caryotype = request.POST.get('caryotype')
            bilan_thyroidien = request.POST.get('bilan_thyroidien')

            # Pathologie endocrinienne
            pathologie_endocrinienne = request.POST.get('pathologie_endocrinienne')
            age_pathologie_endocrinienne = request.POST.get('age_pathologie_endocrinienne')
            diabete = request.POST.get('diabete')
            age_diabete = request.POST.get('age_diabete')
            obesite = request.POST.get('obesite')
            obesite_dates = request.POST.getlist('obesite_date[]')
            obesite_poids = request.POST.getlist('obesite_poids[]')  # kg
            obesite_taille = request.POST.getlist('obesite_taille[]')  # cm (1/100 pour m)

            # Pathologie cardiaque
            echo_coeur_fait = request.POST.get('echo_coeur_fait')
            echo_coeur_type = request.POST.get('echo_coeur_type')
            commentairePCardiaque = request.POST.get('commentairePCardiaque')
            opere = request.POST.get('opere')
            opere_dates = request.POST.getlist('opere_date[]')
            opere_types = request.POST.getlist('opere_type[]')
            opere_suivis = request.POST.get('opere_suivi')
            opere_suivi_dates = request.POST.getlist('opere_suivi_date[]')

            # Pathologie digestif
            reflux_gastro_oesophagien = request.POST.get('reflux_gastro_oesophagien')
            maladie_coeliaque = request.POST.get('maladie_coeliaque')
            agedebut_maladie_coalique = request.POST.get('agedebut_maladie_coalique')
            mucoviscidose = request.POST.get('mucoviscidose')

            # Pathologie ophtalmologique
            pathologie_ophtalmologique = request.POST.get('pathologie_ophtalmologique')

            # Pathologie ORL
            pathologie_orl = request.POST.get('pathologie_orl')

            # Pathologie suivi dentaire
            pathologie_suivie_dentaire = request.POST.get('pathologie_suivie_dentaire')
            pathologie_suivie_dentaire_Commentaire = request.POST.get('pathologie_suivie_dentaire_Commentaire')
            dates_acts = request.POST.getlist('dates_acts[]')
            dent_GaucheDroit = request.POST.getlist('dent_GaucheDroit[]')
            dent_HautBas = request.POST.getlist('dent_HautBas[]')
            dent_num = request.POST.getlist('dent_num[]')
            codes_acts = request.POST.getlist('codes_acts[]')

            # Pathologie osteoarticulaire
            pathologie_osteoarticulaire = request.POST.get('pathologie_osteoarticulaire')

            # Pathologie neurologique
            pathologie_neurologique = request.POST.get('pathologie_neurologique')
            epilepsie = request.POST.get('epilepsie')
            imagerie_faite = request.POST.get('imagerie_faite')

            # Autre Pathologie
            autre_pathologie = request.POST.get('autre_pathologie')
            traitement = request.POST.get('traitement')

            # Hernies
            hernies = request.POST.get('hernies')
            typeHernie_direction = request.POST.get('typeHernie_direction')

            # Suivi paraclinique : Psychomotricien
            Psychomotricien_type = request.POST.get('Psychomotricien_type')
            Psychomotricien_agedebut = request.POST.get('Psychomotricien_agedebut')
            Psychomotricien_frequenceensemaine = request.POST.get('Psychomotricien_frequenceensemaine')
            Psychomotricien_commentaire = request.POST.get('Psychomotricien_commentaire')

            # Suivi paraclinique : Kinésithérapie fonctionnelle
            Kinesitherapie_fonctionnelle_type = request.POST.get('Kinesitherapie_fonctionnelle_type')
            Kinesitherapie_fonctionnelle_agedebut = request.POST.get('Kinesitherapie_fonctionnelle_agedebut')
            Kinesitherapie_fonctionnelle_frequenceensemaine = request.POST.get(
                'Kinesitherapie_fonctionnelle_frequenceensemaine')
            Kinesitherapie_fonctionnelle_commentaire = request.POST.get('Kinesitherapie_fonctionnelle_commentaire')

            # Suivi paraclinique : Psychologue
            Psychologue_type = request.POST.get('Psychologue_type')
            Psychologue_agedebut = request.POST.get('Psychologue_agedebut')
            Psychologue_frequenceensemaine = request.POST.get('Psychologue_frequenceensemaine')
            Psychologue_commentaire = request.POST.get('Psychologue_commentaire')

            # Suivi paraclinique : Orthophoniste
            Orthophoniste_type = request.POST.get('Orthophoniste_type')
            Orthophoniste_agedebut = request.POST.get('Orthophoniste_agedebut')
            Orthophoniste_frequenceensemaine = request.POST.get('Orthophoniste_frequenceensemaine')
            Orthophoniste_commentaire = request.POST.get('Orthophoniste_commentaire')

            # Suivi paraclinique : Orthoptiste
            Orthoptiste_type = request.POST.get('Orthoptiste_type')
            Orthoptiste_agedebut = request.POST.get('Orthoptiste_agedebut')
            Orthoptiste_frequenceensemaine = request.POST.get('Orthoptiste_frequenceensemaine')
            Orthoptiste_commentaire = request.POST.get('Orthoptiste_commentaire')

            # Scolarité et activités
            scolarise = request.POST.get('scolarise')
            scolarise_age_de_début = request.POST.get('scolarise_age_de_debut')
            classe_primaires = request.POST.getlist('classe_primaire[]')
            scolarise_classe_préparatoire = request.POST.get('scolarise_classe_préparatoire')
            classe_primaire_years = request.POST.getlist('classe_primaire_year[]')
            classe_secondaires = request.POST.getlist('classe_secondaires[]')
            classe_secondaire_years = request.POST.getlist('classe_secondaire_years[]')
            bac_years = request.POST.getlist('BAC[]')
            bac_filieres = request.POST.getlist('filiere[]')
            scolarise_bac_choice = request.POST.get('bac_choice')
            scolarise_classe_secondaires_choice = request.POST.get('classe_secondaires_choice')
            scolarise_classe_primaire_choice = request.POST.get('classe_primaire_choice')
            activite_sportive = request.POST.get('activite_sportive')
            activite_artistique = request.POST.get('activite_artistique')
            activite_prof = request.POST.get('activite_prof')
            APr = request.POST.getlist('APr[]')
            AAr = request.POST.getlist('AAr[]')
            ASp = request.POST.getlist('ASp[]')

            if couvertureMedicale == "NonMutualiste":
                nomCouvertureMedical = ""
            if scolarise != ("Oui"):
                scolarise_classe_secondaires_choice = ""
                scolarise_classe_primaire_choice = ""
                scolarise_bac_choice = ""

            if request.user.is_authenticated:
                inpePediatre = request.user
                pediatre = Pediatre.objects.get(user=inpePediatre)

                try:
                    idPatientNew = get_and_update_generate_id()
                except BaseException as e:
                    redirect('home_pediatre')
                else:
                    # Creation d'une instance User
                    # usernamePatient = nom.upper() + "." + prenom.upper()
                    user = User.objects.create_user(username=idPatientNew, first_name=prenom, last_name=nom,
                                                    email=mailPatient, is_patient=True)
                    user.set_password(datenaissance)
                    if user:
                        user.save()
                        if imgPatient is not None:
                            fs = FileSystemStorage(location='Uploads/imgProfile_patient/')
                            image_extention = os.path.splitext(imgPatient.name)[1][1:].lower()
                            imgPatientName = fs.save(f'{idPatientNew}.{image_extention}', imgPatient)
                            imgPatientAdresse = '/' + imgPatientName

                            patientUser = Patient(user=user, idPatient=idPatientNew, inpe=pediatre,
                                                  passwordPatient=datenaissance, nomPatient=nom, prenomPatient=prenom,
                                                  sexePatient=sexe,
                                                  dateNaissancePatient=datenaissance,
                                                  mailPatient=mailPatient, adressePatient=adresse,
                                                  numTelephoneMere=teleMom,
                                                  numTelephonePere=teleDad, villePatient=ville,
                                                  delegationPatient=delegation,
                                                  couvertureMedical=couvertureMedicale,
                                                  nomCouvertureMedical=nomCouvertureMedical,
                                                  imgPatient=imgPatientAdresse)
                        else:
                            patientUser = Patient(user=user, idPatient=idPatientNew, inpe=pediatre,
                                                  passwordPatient=datenaissance, nomPatient=nom, prenomPatient=prenom,
                                                  sexePatient=sexe,
                                                  dateNaissancePatient=datenaissance,
                                                  mailPatient=mailPatient, adressePatient=adresse,
                                                  numTelephoneMere=teleMom,
                                                  numTelephonePere=teleDad, villePatient=ville,
                                                  delegationPatient=delegation,
                                                  couvertureMedical=couvertureMedicale,
                                                  nomCouvertureMedical=nomCouvertureMedical)

                        if patientUser:
                            patientUser.save()
                            infoPatientUser = InfoPatient(patient=patientUser, parents_Consanguins=parents_Consanguins,
                                                          age_maternel_accouchement=age_maternel_accouchement,
                                                          grossesse_suivi=grossesse_suivi,
                                                          terme_grossesse=terme_grossesse,
                                                          precisionTerme=precisionTerme,
                                                          accouchement_par_voie=accouchement_par_voie,
                                                          souffrance_neonatal=souffrance_neonatal,
                                                          poids_de_naissance=poids_de_naissance,
                                                          taille_de_naissance=taille_de_naissance,
                                                          Notion_hospitalisation_age_neonatal=Notion_hospitalisation_age_neonatal,
                                                          allaitement=allaitement,
                                                          diversification_alimentaire=diversification_alimentaire,
                                                          retentissement_staturo_ponderale=retentissement_staturo_ponderale,
                                                          assis_avec_appui=assis_avec_appui,
                                                          assis_sans_appui=assis_sans_appui,
                                                          marche_serpant=marche_serpant,
                                                          marche_4_pattes=marche_4_pattes,
                                                          debout_sans_appui=debout_sans_appui,
                                                          debout_avec_appui=debout_avec_appui,
                                                          parole_syllabe=parole_syllabe, parole_mots=parole_mots,
                                                          parole_phrase=parole_phrase,
                                                          interaction_avec_entourage=interaction_avec_entourage,
                                                          trouble_de_concentration=trouble_de_concentration,
                                                          trouble_de_comportement=trouble_de_comportement,
                                                          spectre_autisme=spectre_autisme, caryotype=caryotype,
                                                          potentiel_evoque_auditif=potentiel_evoque_auditif,
                                                          bilan_thyroidien=bilan_thyroidien,

                                                          pathologie_endocrinienne=pathologie_endocrinienne,
                                                          age_pathologie_endocrinienne=age_pathologie_endocrinienne,
                                                          diabete=diabete, age_diabete=age_diabete, obesite=obesite,

                                                          echo_coeur_fait=echo_coeur_fait,
                                                          echo_coeur_type=echo_coeur_type, opere=opere,
                                                          commentairePCardiaque=commentairePCardiaque,

                                                          reflux_gastro_oesophagien=reflux_gastro_oesophagien,
                                                          maladie_coeliaque=maladie_coeliaque,
                                                          agedebut_maladie_coalique=agedebut_maladie_coalique,
                                                          mucoviscidose=mucoviscidose,

                                                          hernies=hernies,
                                                          typeHernie_direction=typeHernie_direction,

                                                          pathologie_ophtalmologique=pathologie_ophtalmologique,
                                                          pathologie_orl=pathologie_orl,
                                                          pathologie_osteoarticulaire=pathologie_osteoarticulaire,

                                                          pathologie_suivie_dentaire_Commentaire=pathologie_suivie_dentaire_Commentaire,
                                                          pathologie_suivie_dentaire=pathologie_suivie_dentaire,

                                                          pathologie_neurologique=pathologie_neurologique,
                                                          epilepsie=epilepsie,
                                                          imagerie_faite=imagerie_faite,

                                                          traitement=traitement,
                                                          autre_pathologie=autre_pathologie,

                                                          Psychologue_type=Psychologue_type,
                                                          Psychologue_agedebut=Psychologue_agedebut,
                                                          Psychologue_frequenceensemaine=Psychologue_frequenceensemaine,
                                                          Psychologue_commentaire=Psychologue_commentaire,

                                                          Orthophoniste_type=Orthophoniste_type,
                                                          Orthophoniste_agedebut=Orthophoniste_agedebut,
                                                          Orthophoniste_frequenceensemaine=Orthophoniste_frequenceensemaine,
                                                          Orthophoniste_commentaire=Orthophoniste_commentaire,

                                                          Psychomotricien_type=Psychomotricien_type,
                                                          Psychomotricien_agedebut=Psychomotricien_agedebut,
                                                          Psychomotricien_frequenceensemaine=Psychomotricien_frequenceensemaine,
                                                          Psychomotricien_commentaire=Psychomotricien_commentaire,

                                                          Kinesitherapie_fonctionnelle_type=Kinesitherapie_fonctionnelle_type,
                                                          Kinesitherapie_fonctionnelle_agedebut=Kinesitherapie_fonctionnelle_agedebut,
                                                          Kinesitherapie_fonctionnelle_frequenceensemaine=Kinesitherapie_fonctionnelle_frequenceensemaine,
                                                          Kinesitherapie_fonctionnelle_commentaire=Kinesitherapie_fonctionnelle_commentaire,

                                                          Orthoptiste_type=Orthoptiste_type,
                                                          Orthoptiste_agedebut=Orthoptiste_agedebut,
                                                          Orthoptiste_frequenceensemaine=Orthoptiste_frequenceensemaine,
                                                          Orthoptiste_commentaire=Orthoptiste_commentaire,

                                                          scolarise=scolarise,
                                                          scolarise_age_de_début=scolarise_age_de_début,
                                                          scolarise_classe_préparatoire=scolarise_classe_préparatoire,
                                                          scolarise_bac_choice=scolarise_bac_choice,
                                                          scolarise_classe_secondaires_choice=scolarise_classe_secondaires_choice,
                                                          scolarise_classe_primaire_choice=scolarise_classe_primaire_choice,
                                                          activite_sportive=activite_sportive,
                                                          activite_artistique=activite_artistique,
                                                          activite_prof=activite_prof)
                            if infoPatientUser:
                                infoPatientUser.save()

                                if pathologie_suivie_dentaire == "Oui":
                                    for x in range(0, len(dates_acts)):
                                        pathologieDentaire = PathologieDentaire(patientID=idPatientNew,
                                                                               date_act=dates_acts[x],
                                                                               dent_GaucheDroit=dent_GaucheDroit[x],
                                                                               dent_HautBas=dent_HautBas[x],
                                                                               dent_num=dent_num[x],
                                                                               code_act=codes_acts[x])
                                        pathologieDentaire.save()

                                if opere == ("Oui"):
                                    osd = 0
                                    for x in range(0, len(opere_dates)):
                                        patientOpere = PathologieCardiqueOpere(patientID=idPatientNew,
                                                                               opere_date=opere_dates[x],
                                                                               opere_type=opere_types[x],
                                                                               opere_suivi=opere_suivis[x])
                                        patientOpere.save()
                                        if patientOpere.opere_suivi == "Oui":
                                            patientOpere.opere_suivi_date = opere_suivi_dates[osd]
                                            osd = osd + 1
                                            patientOpere.save()

                                if obesite == ("Oui"):
                                    for x in range(0, len(obesite_dates)):
                                        patientObesite = ObesiteImc(patientID=patientUser.idPatient,
                                                                    obesite_date=obesite_dates[x],
                                                                    obesite_poids=obesite_poids[x],
                                                                    obesite_taille=obesite_taille[x],
                                                                    imc=round(float(obesite_poids[x]) / ((float(obesite_taille[x]) / 100) ** 2), 3))
                                        patientObesite.save()
                                if (activite_prof == ("Oui")):
                                    for x in APr:
                                        patientActivite = PatientActivite(patientID=patientUser.idPatient,
                                                                          type_activite="Activite professionnel",
                                                                          description_activite=x)
                                        patientActivite.save()
                                if (activite_artistique == ("Oui")):
                                    for x in AAr:
                                        patientActivite = PatientActivite(patientID=patientUser.idPatient,
                                                                          type_activite="Activite artistique",
                                                                          description_activite=x)
                                        patientActivite.save()
                                if (activite_sportive == ("Oui")):
                                    for x in ASp:
                                        patientActivite = PatientActivite(patientID=patientUser.idPatient,
                                                                          type_activite="Activite sportive",
                                                                          description_activite=x)
                                        patientActivite.save()
                                if scolarise == ("Oui"):
                                    if scolarise_classe_primaire_choice == ("on"):
                                        for x in range(0, len(classe_primaires)):
                                            patientScolaritePrimaire = PatientScolarite(patientID=patientUser.idPatient,
                                                                                        type_scolarite="Classe primaire",
                                                                                        level_scolarite=
                                                                                        classe_primaires[x],
                                                                                        year_scolarite=
                                                                                        classe_primaire_years[x])
                                            patientScolaritePrimaire.save()

                                    if scolarise_classe_secondaires_choice == ("on"):
                                        for x in range(0, len(classe_secondaires)):
                                            patientScolariteSecondaire = PatientScolarite(
                                                patientID=patientUser.idPatient,
                                                type_scolarite="Classe secondaire",
                                                level_scolarite=classe_secondaires[x],
                                                year_scolarite=classe_secondaire_years[x])
                                            patientScolariteSecondaire.save()

                                    if scolarise_bac_choice == ("on"):
                                        for x in range(0, len(bac_filieres)):
                                            patientScolariteBac = PatientScolarite(patientID=patientUser.idPatient,
                                                                                   type_scolarite="BAC",
                                                                                   level_scolarite=bac_filieres[x],
                                                                                   year_scolarite=bac_years[x])
                                            patientScolariteBac.save()

                                return redirect('afficher_infos_patient', patient_id=idPatientNew)
                            else:
                                user.delete()
                                patientUser.delete()
                        else:
                            user.delete()
                    error = "Impossible de creer l'utilisateur"
                    errorValue = True
            else:
                return redirect('login_pediatre')
        else:
            if 'submitted' in request.GET:
                submitted = True
            delegations = Delegation.objects.values_list('nomDelegation', flat=True)
            CPr = ClassePrimaire.objects.values_list('classePName', flat=True)
            CSr = ClasseSecondaire.objects.values_list('classeSName', flat=True)
            mutuelles = Mutuelle.objects.values_list('mutuelleName', flat=True).order_by('mutuelleName')
            context = {
                'CPr': list(CPr),
                'CSr': list(CSr),
                'submitted': submitted,
                'error': error,
                'errorValue': errorValue,
                'delegations': list(delegations),
                'mutuelles': list(mutuelles),
            }

        return render(request, 'Pediatre/ajouterPatient_pediatre.html', context)
    else:
        return redirect('login_pediatre')


def classes_ajax(request):
    CPr = ClassePrimaire.objects.order_by('idClassePrimaire').values_list('classePName', flat=True)
    CSr = ClasseSecondaire.objects.order_by('idClasseSecondaire').values_list('classeSName', flat=True)
    context = {
        'CPr': list(CPr),
        'CSr': list(CSr),
    }
    return JsonResponse(context)


def delegationCities_ajax(request):
    selectedValue = request.GET.get('selectedValue', '')
    delegationInstance = Delegation.objects.get(nomDelegation=selectedValue)
    listCities = Ville.objects.filter(delegation=delegationInstance)
    cityNames = listCities.values_list('nomVille', flat=True)
    return JsonResponse({'cityNames': list(cityNames)})


def home_pediatre(request):
    patients = []
    error = request.GET.get('error')
    errorValue = request.GET.get('errorValue')
    if error is None:
        error = ""
    if errorValue is None:
        errorValue = False
    if request.user.is_authenticated:
        try:
            pediatre = Pediatre.objects.get(user=request.user)
            patients = Patient.objects.filter(inpe=pediatre, is_deleted="Non")
        except BaseException as e:
            error = str(e)
            errorValue = True
        else:
            context = {
                'error': error,
                'errorValue': errorValue,
                'patients': patients,
            }
            return render(request, 'Pediatre/mesPatients_pediatre.html', context)
    else:
        return redirect('login_pediatre')


def index_pediatre(request):
    if request.user.is_authenticated:
        return redirect('home_pediatre')
    else:
        return redirect('login_pediatre')


def corbeille_patient(request):
    if request.user.is_authenticated:
        patientDeleteds = CorbeillePatient.objects.all()
        today = timezone.now().date()
        for p in patientDeleteds:
            if (p.dateSuppression_fin == today):
                p.delete()
        context = {
            'patientDeleteds': patientDeleteds,
        }
        return render(request, 'Pediatre/corbeillePatients_pediatre.html', context)
    else:
        return redirect('login_pediatre')


def add_patient_corbeille(request, patient_id):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            patient.is_deleted = "Oui"
            #Desactiver l'user
            patient.user.is_active = False
            patient.user.save()
            patient.save()
            patientDeleted = CorbeillePatient(patient=patient)
            patientDeleted.save()
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
            return redirect('home_pediatre/?error=' + error + '&errorValue=' + str(errorValue))
        else:
            return redirect('home_pediatre')
    else:
        return redirect('login_pediatre')

def restore_patient_corbeille(request, patient_id):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            patient.is_deleted = "Non"
            # Activer l'user
            patient.user.is_active = True
            patient.user.save()
            patient.save()
            patientDeleted = CorbeillePatient.objects.get(patient=patient)
            patientDeleted.delete()
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
            return redirect('home_pediatre/?error=' + error + '&errorValue=' + str(errorValue))
        else:
            return redirect('corbeille_patient')
    else:
        return redirect('login_pediatre')

def login_pediatre(request):
    error = ""
    errorValue = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_pediatre:
            login(request, user)
            return redirect('home_pediatre')
    return render(request, 'loginUsers.html', {'error': error, 'errorValue': errorValue})

def nouveau_pediatre(request):
    error = ""
    errorValue = False
    if request.method == 'POST':
        # Recuperation des infos
        inpe = request.POST['inpe']
        nomPediatre = request.POST['nomPediatre']
        prenomPediatre = request.POST['prenomPediatre']
        numTelephonePediatre = request.POST['numTelephonePediatre']
        mailPediatre = request.POST['mailPediatre']
        adressePediatre = request.POST['adressePediatre']
        cniPediatre = request.POST['cniPediatre']
        password = cniPediatre

        # Craetion d'une instance User
        user = User.objects.create_user(username=inpe,
                                        first_name=prenomPediatre,
                                        last_name=nomPediatre,
                                        email=mailPediatre,
                                        is_pediatre=True)
        user.set_password(password)
        if user:
            user.save()
            pediatreUser = Pediatre(user=user, inpe=inpe, cniPediatre=cniPediatre, nomPediatre=nomPediatre,
                                    prenomPediatre=prenomPediatre, mailPediatre=mailPediatre,
                                    numTelephonePediatre=numTelephonePediatre, adressePediatre=adressePediatre,
                                    passwordPediatre=password)
            if pediatreUser:
                pediatreUser.save()
                registrationValue = True
                registration = "** Pediatre est ajoute avec succes **"
                return render(request, 'Pediatre/nouveauPediatre.html',
                              {'registrationValue': registrationValue, 'registration': registration})
            else:
                user.delete()
        error = "Impossible de creer l'utilisateur"
        errorValue = True
    return render(request, 'Pediatre/nouveauPediatre.html', {'error': error, 'errorValue': errorValue})

def logout_pediatre(request):
    if request.user.is_authenticated:
        try:
            logout(request)
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
            return redirect('home_pediatre/?error=' + error + '&errorValue=' + str(errorValue))
        else:
            return redirect("index_pediatre")
    else:
        return redirect('login_pediatre')

def messagerie_pediatre(request):
    if request.user.is_authenticated:
        boite_reception = []
        nbrVu = 0
        try:
            conversations = Conversation.objects.filter(
                Q(Q(receiver=request.user) | Q(sender=request.user)) | Q(
                    Q(nbrMessage__gte=2) | Q(sender=request.user))).order_by('-dateUpdated').distinct()

            for c in conversations:
                try:
                    #Conter le nbr des msgs qui sont vu par l'utilisateur pour cette conversation
                    message_vu = Message.objects.filter(conversation=c, vu=False, receiver=request.user)
                    #Conter le nbr des messages qui ne sont pas vu par l'user
                    nbrVu = len(message_vu)
                    #Si aucun msg n'est vu je vais pas ajouter un style css
                    if nbrVu == 0:
                        msg_is_vu = True
                    else:
                        msg_is_vu = False

                    #Prendre le dernier message d'une conversation
                    message = Message.objects.filter(conversation=c).latest('dateEnvoie')
                    last_message = message.message
                    if len(last_message) > 112:
                        truncated_msg = last_message[:100]
                        truncated_msg = truncated_msg + "..."
                    else:
                        truncated_msg = last_message
                    print(truncated_msg)

                except Message.DoesNotExist:
                    last_message = None
                    truncated_msg = ""
                boite_reception.append([c, msg_is_vu, nbrVu, truncated_msg, message])
                nbrVu = 0

            context = {
                "boite_reception": boite_reception,
            }
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
            return redirect('home_pediatre/?error=' + error + '&errorValue=' + str(errorValue))
        else:
            return render(request, 'Pediatre/messageriePediatre_pediatre.html', context)
    else:
        return redirect('login_pediatre')

def conversation_pediatre(request, conversation_id):
    if request.user.is_authenticated:
        conversation = Conversation.objects.get(idConversation=conversation_id)
        messages = Message.objects.filter(conversation=conversation).order_by('dateEnvoie')
        for m in messages:
            if (m.receiver == request.user):
                m.vu = True
                m.save()
        context = {
            'conversation': conversation,
            'messages': messages,
            'conversation_id ': conversation_id,
        }
        return render(request, 'Pediatre/conversation_pediatre_pediatre.html', context)
    else:
        return redirect('login_pediatre')

def conversation_pediatre_ajax(request, conversation_id):
    if request.user.is_authenticated:
        context = {}
        conversation = Conversation.objects.get(idConversation=conversation_id)
        messages = Message.objects.filter(conversation=conversation).order_by('dateEnvoie')
        for m in messages:
            if (m.receiver == request.user):
                m.vu = True
                m.save()
        data = []
        for m in messages:
            moi = 'False'
            if m.sender == request.user :
                moi = 'True'
            data.append({
                'moi' : moi,
                'sender': m.sender.last_name + ' ' + m.sender.first_name,
                'message': m.message,
                'dateEnvoie': m.dateEnvoie,
                'msg_is_vu': m.vu,
            })
        return JsonResponse(data, safe=False)
    else:
        return redirect('login_pediatre')

def send_message_pediatre(request, conversation_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            messageChat = request.POST.get('messageChat')
            if messageChat != "":
                conversation = Conversation.objects.get(idConversation=conversation_id)

                receiver = conversation.receiver
                if conversation.receiver == request.user:
                    receiver = conversation.sender

                message = Message(conversation=conversation, receiver=receiver, sender=request.user,
                                  message=messageChat)
                message.save()
                dateUpdate = message.dateEnvoie
                conversation.dateUpdated = dateUpdate
                conversation.save()

            # return a JSON response indicating success
            return JsonResponse({'status': 'ok'})
    else:
        return redirect('login_pediatre')

def recherche_conversation_pediatre(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            boite_reception = []
            try:
                convSearch = request.POST['convSearch']
                conversations = Conversation.objects.filter(
                    Q(receiver__username__icontains=convSearch) |
                    Q(receiver__first_name__icontains=convSearch) |
                    Q(receiver__last_name__icontains=convSearch) |
                    Q(sender__username__icontains=convSearch) |
                    Q(sujet__icontains=convSearch) |
                    Q(dateStart__icontains=convSearch) |
                    Q(dateUpdated__icontains=convSearch)
                )
                print("=====================================================")
                print(conversations)
                for c in conversations:
                    try:
                        # Conter le nbr des msgs qui sont vu par l'utilisateur pour cette conversation
                        message_vu = Message.objects.filter(conversation=c, vu=False, receiver=request.user)
                        # Conter le nbr des messages qui ne sont pas vu par l'user
                        nbrVu = len(message_vu)
                        # Si aucun msg n'est vu je vais pas ajouter un style css
                        if nbrVu == 0:
                            msg_is_vu = True
                        else:
                            msg_is_vu = False

                        # Prendre le dernier message d'une conversation
                        message = Message.objects.filter(conversation=c).latest('dateEnvoie')
                        last_message = message.message
                        if len(last_message) > 112:
                            truncated_msg = last_message[:100]
                            truncated_msg = truncated_msg + "..."
                        else:
                            truncated_msg = last_message
                        print(truncated_msg)

                    except Message.DoesNotExist:
                        last_message = None
                        truncated_msg = ""
                    boite_reception.append([c, msg_is_vu, nbrVu, truncated_msg, message])
                    nbrVu = 0
            except BaseException as e:
                print("Caught exception:", e)
                error = str(e)
                errorValue = True
                conversations = None

        context = {'boite_reception': boite_reception}
        #boite_reception.append([c, msg_is_vu, nbrVu, truncated_msg, message])
        return render(request, 'Pediatre/messageriePediatre_pediatre.html', context)
    else:
        return redirect('login_pediatre')

def new_conversation_pediatre(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            errorValue = False
            error = ""

            destinataire = request.POST['destinataire']
            subject = request.POST['subject']
            message = request.POST['message']

            #Recherche d'username
            try:
                receiver = User.objects.get(username=destinataire)
            except User.DoesNotExist:
                print(f"Error: User '{destinataire}' does not exist")
                errorValue = True
                error = "Error: User '{destinataire}' does not exist"
                context = {
                    'errorValue':errorValue,
                    'error':error,
                }
                return render(request, 'Pediatre/newConversation_Pediatre.html', context)
            else:
                #Creation d'une conversation
                conversation = Conversation(sujet=subject, receiver=receiver, sender=request.user)
                conversation.save()
                message = Message(conversation=conversation, receiver=receiver, sender=request.user,
                                  message=message)
                message.save()

                return redirect('conversation_pediatre', conversation_id=conversation.idConversation)
        else:
            return render(request, 'Pediatre/newConversation_Pediatre.html')
    else:
        return redirect('login_pediatre')