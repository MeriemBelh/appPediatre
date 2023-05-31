import os

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import *
from .models import Administrateur
from Patient.models import *
from Administrateur.models import *
from Pediatre.models import *
from AppPediatre.views import *
from django.contrib.auth import get_user_model

User = get_user_model()
#=================Messagerie======================
def conversation_admin(request, conversation_id):
    if request.user.is_authenticated:
        boite_reception = []
        nbrVu = 0
        try:
            conversations = Conversation.objects.filter(
                Q(Q(receiver=request.user) | Q(sender=request.user)) | Q(
                    Q(nbrMessage__gte=2) | Q(sender=request.user))).order_by('-dateUpdated').distinct()

            conversation = Conversation.objects.get(idConversation=conversation_id)
            messages = Message.objects.filter(conversation=conversation).order_by('dateEnvoie')

            for m in messages:
                if (m.receiver == request.user):
                    m.vu = True
                    m.save()

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
            return redirect('index_admin')
        else:
            context = {
                'conversation': conversation,
                'messages': messages,
                'conversation_id ': conversation_id,
                "boite_reception": boite_reception,
            }
            return render(request, 'Pediatre/conversationAdmin.html', context)
    else:
        return redirect('homPage')

def chatAdmin(request):
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
            return redirect('index_admin')
        else:
            return render(request, 'Administrateur/chatAdmin.html', context)
    else:
        return redirect('homPage')
#----------------------------------------------------Admin--------------------------------------
#-----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def desactiver_admin(request, admin):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            user = User.objects.get(username=admin)
            administrateur = Administrateur.objects.get(user=user)
            user.is_active = False
            user.save()
            administrateur.save()
            return redirect('gestion_administrateurs')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

def activer_admin(request, admin):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            user = User.objects.get(username=admin)
            administrateur = Administrateur.objects.get(user=user)
            user.is_active = True
            user.save()
            administrateur.save()
            return redirect('gestion_patients')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

def supprimer_admin(request, admin):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            user = User.objects.get(username=admin)
            user.delete()
            # Redirect
            return redirect('gestion_administrateurs')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

def editer_admin(request, admin):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        user = User.objects.get(username=admin)
        administrateur = Administrateur.objects.get(user=user)
        # ---------------------------------Pour le get Methode-----------------

        context = {
            'nomAdmin': administrateur.nomAdmin,
            'prenomAdmin':administrateur.prenomAdmin,
            'passwordAdmin': administrateur.passwordAdmin,
            'mailAdmin':administrateur.mailAdmin,
            'admin':administrateur,
            'username':user.username,
        }
        # --------------Post method----------------------
        if request.method == "POST":
            nomAdmin = request.POST.get('nomAdmin')
            prenomAdmin = request.POST.get('prenomAdmin')
            passwordAdmin = request.POST.get('passwordAdmin')
            mailAdmin = request.POST.get('mailAdmin')

            user = User.objects.get(username=admin)
            administrateur = Administrateur.objects.get(user=user)

            # Changement de mot de passe:
            if passwordAdmin != administrateur.passwordAdmin:
                user.set_password(passwordAdmin)

            usernameAdmin = str(prenomAdmin) + "_" + str(nomAdmin) + ".admin"
            user.first_name = prenomAdmin
            user.last_name = nomAdmin
            user.email = mailAdmin
            user.username = usernameAdmin
            user.save()


            administrateur.nomAdmin = nomAdmin
            administrateur.prenomAdmin = prenomAdmin
            administrateur.passwordAdmin = passwordAdmin
            administrateur.mailAdmin = mailAdmin
            administrateur.save()


            url = reverse('afficher_administrateur', args=[admin])
            return redirect(url)

        return render(request, 'Administrateur/editer_admin.html', context)
    else:
        return redirect('homPage')

def recherche_administrateur(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        patients = []
        context = {}

        try:
            admin_bd = Administrateur.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
        else:
            # --------------Post method----------------------
            if request.method == "POST":
                nom = request.POST.get('nom')
                mail = request.POST.get('mail')

                query = Q()
                if nom:
                    query &= (Q(nomAdmin__icontains=nom) | Q(prenomAdmin__icontains=nom))
                if mail:
                    query &= Q(mailAdmin__icontains=mail)

                admin_bd = Administrateur.objects.filter(query)

                context = {
                    'error': error,
                    'errorValue': errorValue,
                    'administrateurs': admin_bd,
                }

        return render(request, "Administrateur/rechercheAdministrateurs.html", context)
    else:
        return redirect('homPage')

def gestion_administrateurs(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        patients = []
        context = {}

        try:
            admin_bd = Administrateur.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
        else:
            context = {
                'error': error,
                'errorValue': errorValue,
                'administrateurs': admin_bd,
            }
        return render(request, "Administrateur/administrateursListe_admin.html", context)
    else:
        return redirect('homPage')

def ajouter_administrateur(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        context = {}
        # --------------Post method----------------------
        if request.method == "POST":
            nomAdmin = request.POST.get('nomAdmin')
            passwordAdmin = request.POST.get('passwordAdmin')
            mailAdmin = request.POST.get('mailAdmin')
            prenomAdmin = request.POST.get('prenomAdmin')

            usernameAdmin = str(prenomAdmin) + "_" + str(nomAdmin) + ".admin"

            # Craetion d'une instance User
            user = User.objects.create_user(username=usernameAdmin,
                                            first_name=prenomAdmin,
                                            last_name=nomAdmin,
                                            email=mailAdmin,
                                            is_admin=True)
            user.set_password(passwordAdmin)
            if user:
                user.save()
                adminUser = Administrateur(user=user, nomAdmin=nomAdmin,
                                           prenomAdmin=prenomAdmin,
                                           passwordAdmin=passwordAdmin,
                                           mailAdmin=mailAdmin)
                if adminUser:
                    adminUser.save()
                    url = reverse('afficher_administrateur', args=[user.username])
                    return redirect(url)
                else:
                    user.delete()
                    return redirect('gestion_administrateurs')

        return render(request, 'Administrateur/ajouter_administrateur.html', context)
    else:
        return redirect('homPage')

def afficher_administrateur(request, admin):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            user = User.objects.get(username=admin)
            administrateur = Administrateur.objects.get(user=user)
            context = {
                'admin': administrateur,
            }
            return render(request, "Administrateur/afficher_admin.html", context)
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

#============================================Statistiques============================
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
def statistiques(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        return render(request, 'Administrateur/statistiquesAdmin.html')
    else:
        return redirect('homPage')

def pie_chart_sexe(request):
    patients = Patient.objects.all()
    sexe_counts = dict()
    sexe_counts["Masculin"] = 0
    sexe_counts["Féminin"] = 0
    sexe_counts["Autre"] = 0
    for patient in patients:
        sexe = patient.sexePatient
        if sexe in sexe_counts:
            sexe_counts[sexe] += 1
        else:
            sexe_counts[sexe] = 1
    data = [{'sexe': sexe, 'count': count} for sexe, count in sexe_counts.items()]
    return JsonResponse(data, safe=False)

def pie_chart_region(request):
    patients = Patient.objects.all()
    regions_bd = Delegation.objects.all()

    region_counts = dict()
    """
    for r in regions_bd:
        region_counts[r.nomDelegation] = 0
    """
    for patient in patients:
        region = patient.delegationPatient
        if region in region_counts:
            region_counts[region] += 1
        else:
            region_counts[region] = 1
    data1 = [{'region': region, 'count': count} for region, count in region_counts.items()]
    return JsonResponse(data1, safe=False)

def pie_chart_cm(request):
    patients = Patient.objects.all()
    cm_counts = dict()
    cm_counts["Mutualiste"] = 0
    cm_counts["NonMutualiste"] = 0
    for patient in patients:
        cm = patient.couvertureMedical
        if cm in cm_counts:
            cm_counts[cm] += 1
        else:
            cm_counts[cm] = 1
    data2 = [{'cm': cm, 'count': count} for cm, count in cm_counts.items()]
    return JsonResponse(data2, safe=False)

def pie_chart_ville(request):
    patients = Patient.objects.all()

    ville_counts = dict()
    for patient in patients:
        ville = patient.villePatient
        if ville in ville_counts:
            ville_counts[ville] += 1
        else:
            ville_counts[ville] = 1
    data3 = [{'ville': ville, 'count': count} for ville, count in ville_counts.items()]
    return JsonResponse(data3, safe=False)

def pie_chart_pc(request):
    patients = Patient.objects.all()
    pc_counts = dict()
    pc_counts["Oui"] = 0
    pc_counts["Non"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        pc = infopatient.parents_Consanguins
        if pc in pc_counts:
            pc_counts[pc] += 1
        else:
            pc_counts[pc] = 1
    data4 = [{'pc': pc, 'count': count} for pc, count in pc_counts.items()]
    return JsonResponse(data4, safe=False)

def pie_chart_gs(request):
    patients = Patient.objects.all()
    gs_counts = dict()
    gs_counts["Oui"] = 0
    gs_counts["Non"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        gs = infopatient.grossesse_suivi
        if gs in gs_counts:
            gs_counts[gs] += 1
        else:
            gs_counts[gs] = 1
    data4 = [{'gs': gs, 'count': count} for gs, count in gs_counts.items()]
    return JsonResponse(data4, safe=False)

def pie_chart_tg(request):
    patients = Patient.objects.all()
    tg_counts = dict()
    tg_counts["A terme"] = 0
    tg_counts["Prématuré"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        tg = infopatient.terme_grossesse
        if tg in tg_counts:
            tg_counts[tg] += 1
        else:
            tg_counts[tg] = 1
    data4 = [{'tg': tg, 'count': count} for tg, count in tg_counts.items()]
    return JsonResponse(data4, safe=False)

def pie_chart_av(request):
    patients = Patient.objects.all()
    av_counts = dict()
    av_counts["Basse"] = 0
    av_counts["Césarienne"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        av = infopatient.accouchement_par_voie
        if av in av_counts:
            av_counts[av] += 1
        else:
            av_counts[av] = 1
    data4 = [{'av': av, 'count': count} for av, count in av_counts.items()]
    return JsonResponse(data4, safe=False)

def pie_chart_sn(request):
    patients = Patient.objects.all()
    sn_counts = dict()
    sn_counts["Oui"] = 0
    sn_counts["Non"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        sn = infopatient.souffrance_neonatal
        if sn in sn_counts:
            sn_counts[sn] += 1
        else:
            sn_counts[sn] = 1
    data4 = [{'sn': sn, 'count': count} for sn, count in sn_counts.items()]
    return JsonResponse(data4, safe=False)

def pie_chart_pn(request):
    patients = Patient.objects.all()
    pn_counts = dict()
    pn_counts["< 2Kg"] = 0
    pn_counts["2--2,5Kg"] = 0
    pn_counts["2,5--4Kg"] = 0
    pn_counts["> 4Kg"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        pn = infopatient.poids_de_naissance
        if pn in pn_counts:
            pn_counts[pn] += 1
        else:
            pn_counts[pn] = 1
    data4 = [{'pn': pn, 'count': count} for pn, count in pn_counts.items()]
    return JsonResponse(data4, safe=False)


def pie_chart_han(request):
    patients = Patient.objects.all()
    han_counts = dict()
    han_counts["Oui"] = 0
    han_counts["Non"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        han = infopatient.Notion_hospitalisation_age_neonatal
        if han in han_counts:
            han_counts[han] += 1
        else:
            han_counts[han] = 1
    data4 = [{'han': han, 'count': count} for han, count in han_counts.items()]
    return JsonResponse(data4, safe=False)


def pie_chart_allaitement(request):
    patients = Patient.objects.all()
    allaitement_counts = dict()
    allaitement_counts["Maternel"] = 0
    allaitement_counts["Mixte"] = 0
    allaitement_counts["Artificiel"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        allaitement = infopatient.allaitement
        if allaitement in allaitement_counts:
            allaitement_counts[allaitement] += 1
        else:
            allaitement_counts[allaitement] = 1
    data4 = [{'allaitement': allaitement, 'count': count} for allaitement, count in allaitement_counts.items()]
    return JsonResponse(data4, safe=False)


def pie_chart_rsp(request):
    patients = Patient.objects.all()
    rsp_counts = dict()
    rsp_counts["Retard"] = 0
    rsp_counts["Stagnation"] = 0
    rsp_counts["Bon"] = 0
    for patient in patients:
        infopatient = InfoPatient.objects.get(patient=patient)
        rsp = infopatient.retentissement_staturo_ponderale
        if rsp in rsp_counts:
            rsp_counts[rsp] += 1
        else:
            rsp_counts[rsp] = 1
    data4 = [{'rsp': rsp, 'count': count} for rsp, count in rsp_counts.items()]
    return JsonResponse(data4, safe=False)

#----------------------------------------------------Patient--------------------------------------
#-----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#line chart
def line_chart_Obesite(request, patient_id):
    # Retrieve patient and obesite data
    patient = Patient.objects.get(idPatient=patient_id)
    obesite_data = ObesiteImc.objects.filter(patientID=patient.idPatient).order_by('obesite_date')

    # Prepare data for the chart
    x_axis = []  # X-axis labels (age in months)
    y_axis_poids = []  # Y-axis values for obesite_poids
    y_axis_taille = []  # Y-axis values for obesite_taille
    y_axis_imc = []  # Y-axis values for imc

    # Calculate age in months for each obesite point
    for obesite in obesite_data:
        age = (obesite.obesite_date.year - patient.dateNaissancePatient.year) * 12 + (
                    obesite.obesite_date.month - patient.dateNaissancePatient.month)
        x_axis.append(age)
        y_axis_poids.append(obesite.obesite_poids)
        y_axis_taille.append(obesite.obesite_taille)
        y_axis_imc.append(obesite.imc)

    # Render the chart using C3.js
    chart_data = {
        'x': 'x',
        'columns': [
            ['x'] + x_axis,
            ['obesite_poids'] + y_axis_poids,
            ['obesite_taille'] + y_axis_taille,
            ['imc'] + y_axis_imc,
        ],
    }
    return JsonResponse(chart_data)

# Afficher patient
def afficher_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            userPatient = Patient.objects.get(idPatient=patient_id)
            infopatient = InfoPatient.objects.get(patient=userPatient)
            file_name = os.path.basename(userPatient.imgPatient.url)
            img_path = "/imgProfile_patient/" + file_name

            context = {
                'p':userPatient,
                'img': img_path,
                'infopatient':infopatient,
            }
            return render(request, "Administrateur/afficherPatient_admin.html",context)
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

# Ajouter patient
def ajouter_patient(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        context = {}
        # ---------------------------------Pour le get Methode-----------------
        try:
            delegations = Delegation.objects.values_list('nomDelegation', flat=True)
            mutuelles = Mutuelle.objects.values_list('mutuelleName', flat=True).order_by('mutuelleName')
            pediatres = Pediatre.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
            print(error)
        else:
            context = {
                'error': error,
                'errorValue': errorValue,
                'delegations': list(delegations),
                'mutuelles': list(mutuelles),
                'pediatres':pediatres,
            }
        # --------------Post method----------------------
        if request.method == "POST":
            imgPatient = request.FILES.get('imgPatient')
            nomPatient = request.POST.get('nompatient')
            dateNaissancePatient = request.POST.get('dateNaissancePatient')
            numTelephoneMere = request.POST.get('telemaman')
            prenomPatient = request.POST.get('prenompatient')
            sexepatient = request.POST.get('sexepatient')
            numTelephonePere = request.POST.get('telepapa')
            mailPatient = request.POST.get('mailpatient')
            adressePatient = request.POST.get('adressepatient')
            delegationPatient = request.POST.get('regionpatient')
            villePatient = request.POST.get('villepatient')
            mutualiste = request.POST.get('mutualiste')
            mutuelepatient = request.POST.get('mutuelepatient')
            pediatreInpe = request.POST.get('pediatre')

            parents_Consanguins = request.POST.get('parents_Consanguins')
            age_maternel_accouchement = request.POST.get('age_maternel_accouchement')
            grossesse_suivi = request.POST.get('grossesse_suivi')
            terme_grossesse = request.POST.get('terme_grossesse')
            precisionTerme = request.POST.get('precisionTerme')
            accouchement_par_voie = request.POST.get('accouchement_par_voie')
            Notion_hospitalisation_age_neonatal = request.POST.get('Notion_hospitalisation_age_neonatal')
            diversification_alimentaire = request.POST.get('diversification_alimentaire')
            souffrance_neonatal = request.POST.get('souffrance_neonatal')
            poids_de_naissance = request.POST.get('poids_de_naissance')
            taille_de_naissance = request.POST.get('taille_de_naissance')
            allaitement = request.POST.get('allaitement')
            retentissement_staturo_ponderale = request.POST.get('retentissement_staturo_ponderale')

            try:
                idPatientNew = get_and_update_generate_id()
                pediatre = Pediatre.objects.get(inpe=pediatreInpe)
            except BaseException as e:
                redirect('home_pediatre')
            else:
                user = User.objects.create_user(username=idPatientNew, first_name=prenomPatient, last_name=nomPatient,
                                                email=mailPatient, is_patient=True)
                user.set_password(dateNaissancePatient)
                if user:
                    user.save()

                    patientUser = Patient(user=user, idPatient=idPatientNew, inpe=pediatre,
                                          passwordPatient=dateNaissancePatient, nomPatient=nomPatient, prenomPatient=prenomPatient,
                                          sexePatient=sexepatient,
                                          dateNaissancePatient=dateNaissancePatient,
                                          mailPatient=mailPatient, adressePatient=adressePatient,
                                          numTelephoneMere=numTelephoneMere,
                                          numTelephonePere=numTelephonePere, villePatient=villePatient,
                                          delegationPatient=delegationPatient,)
                    if patientUser:
                        patientUser.save()

                        if mutualiste == 'on':
                            patientUser.couvertureMedical = "Mutualiste"
                            patientUser.nomCouvertureMedical = mutuelepatient
                        else:
                            patientUser.couvertureMedical = "NonMutualiste"
                            patientUser.nomCouvertureMedical = " "

                        if imgPatient is not None:
                            fs = FileSystemStorage(location='Uploads/imgProfile_patient/')
                            image_extention = os.path.splitext(imgPatient.name)[1][1:].lower()
                            imgPatientName = fs.save(f'{idPatientNew}.{image_extention}', imgPatient)
                            imgPatientAdresse = '/' + imgPatientName

                            patientUser.imgPatient=imgPatientAdresse

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
                                                      retentissement_staturo_ponderale=retentissement_staturo_ponderale,)
                        if infoPatientUser:
                            infoPatientUser.save()

                            url = reverse('afficher_patient', args=[idPatientNew])
                            return redirect(url)

            return redirect('gestion_patients')

        return render(request, 'Administrateur/ajouter_patient.html', context)
    else:
        return redirect('homPage')

# Supprimer patient
def supprimer_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
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

            # Redirect
            return redirect('gestion_patients')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

# Desactiver patient
def desactiver_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            userPatient = User.objects.get(username=patient_id)
            userPatient.is_active = False
            userPatient.save()
            return redirect('gestion_patients')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

# Activer patient
def activer_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        try:
            userPatient = User.objects.get(username=patient_id)
            userPatient.is_active = True
            userPatient.save()
            return redirect('gestion_patients')
        except BaseException as e:
            errorMessage = str(e)
            errorValue = True
            print(str(e))
            return redirect('homPage')
    else:
        return redirect('homPage')

# Gestion patients
def gestion_patients(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        patients = []
        context = {}

        try:
            patient_bd = Patient.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
        else:
            for p in patient_bd:
                file_name = os.path.basename(p.imgPatient.url)
                img_path = "/imgProfile_patient/" + file_name
                patients.append([p, img_path])
            context = {
                'error': error,
                'errorValue': errorValue,
                'patients': patients,
            }
        return render(request, "Administrateur/patientsListe_admin.html", context)
    else:
        return redirect('homPage')

# Editer patient
def editer_patient(request, patient_id):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        context = {}
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
        # ---------------------------------Pour le get Methode-----------------
        try:
            patient = Patient.objects.get(idPatient=patient_id)
            infopatient = InfoPatient.objects.get(patient=patient)
            villes = Ville.objects.values_list('nomVille', flat=True)
            delegations = Delegation.objects.values_list('nomDelegation', flat=True)
            mutuelles = Mutuelle.objects.values_list('mutuelleName', flat=True).order_by('mutuelleName')
            userPatient = User.objects.get(username=patient_id)
            pediatres = Pediatre.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
            print(error)
            patient = None
            infopatient = None
            userPatient = None
        else:
            dateNaissancePatient = str(patient.dateNaissancePatient)
            context = {
                "p": patient,
                "patient_id": patient_id,
                'error': error,
                'errorValue': errorValue,
                'delegations': list(delegations),
                'mutuelles': list(mutuelles),
                'pediatres': list(pediatres),
                'infopatient': infopatient,
                'dateNaissancePatient': dateNaissancePatient,
                'villes': villes,
                'TROUBLEDIGESTIF': TROUBLEDIGESTIF,
                'POIDSNAISSANCE': POIDSNAISSANCE,
                'ALLAITEMENT': ALLAITEMENT,
                'CARYOTYPE': CARYOTYPE,
                'POTENTIELAUDITIF': POTENTIELAUDITIF,
                'RETENTISSEMENT': RETENTISSEMENT,
            }
        # --------------Post method----------------------
        if request.method == "POST":
            imgPatient = request.FILES.get('imgPatient')
            nomPatient = request.POST.get('nompatient')
            dateNaissancePatient = request.POST.get('dateNaissancePatient')
            numTelephoneMere = request.POST.get('telemaman')
            prenomPatient = request.POST.get('prenompatient')
            sexepatient = request.POST.get('sexepatient')
            numTelephonePere = request.POST.get('telepapa')
            mailPatient = request.POST.get('mailpatient')
            adressePatient = request.POST.get('adressepatient')
            delegationPatient = request.POST.get('regionpatient')
            villePatient = request.POST.get('villepatient')
            mutualiste = request.POST.get('mutualiste')
            mutuelepatient = request.POST.get('mutuelepatient')
            pediatreInpe = request.POST.get('pediatre')
            passwordpatient = request.POST.get('passwordpatient')

            parents_Consanguins = request.POST.get('parents_Consanguins')
            age_maternel_accouchement = request.POST.get('age_maternel_accouchement')
            grossesse_suivi = request.POST.get('grossesse_suivi')
            terme_grossesse = request.POST.get('terme_grossesse')
            precisionTerme = request.POST.get('precisionTerme')
            accouchement_par_voie = request.POST.get('accouchement_par_voie')
            Notion_hospitalisation_age_neonatal = request.POST.get('Notion_hospitalisation_age_neonatal')
            diversification_alimentaire = request.POST.get('diversification_alimentaire')
            souffrance_neonatal = request.POST.get('souffrance_neonatal')
            taille_de_naissance = request.POST.get('taille_de_naissance')
            poids_de_naissance = request.POST.get('poids_de_naissance')
            allaitement = request.POST.get('allaitement')
            retentissement_staturo_ponderale = request.POST.get('retentissement_staturo_ponderale')

            # Changement de mot de passe:
            if passwordpatient != patient.passwordPatient:
                userPatient.set_password(passwordpatient)

            userPatient.first_name = prenomPatient
            userPatient.last_name = nomPatient
            userPatient.email = mailPatient
            userPatient.save()

            # Changement du patient
            pediatre = Pediatre.objects.get(inpe=pediatreInpe)

            patient.user = userPatient
            patient.inpe = pediatre
            patient.passwordPatient = passwordpatient
            patient.sexePatient = sexepatient
            patient.nomPatient = nomPatient
            patient.prenomPatient = prenomPatient
            patient.dateNaissancePatient = dateNaissancePatient
            patient.mailPatient = mailPatient
            patient.adressePatient = adressePatient
            patient.numTelephoneMere = numTelephoneMere
            patient.numTelephonePere = numTelephonePere
            patient.villePatient = villePatient
            patient.delegationPatient = delegationPatient
            patient.villePatient = villePatient

            if mutualiste == 'on':
                patient.couvertureMedical = "Mutualiste"
                patient.nomCouvertureMedical = mutuelepatient
            else:
                patient.couvertureMedical = "NonMutualiste"
                patient.nomCouvertureMedical = ""

            if imgPatient is not None:
                print("Oui Image")
                fs = FileSystemStorage(location='Uploads/imgProfile_patient/')
                image_extention = os.path.splitext(imgPatient.name)[1][1:].lower()
                imgPatientName = fs.save(f'{patient_id}.{image_extention}', imgPatient)
                imgPatientAdresse = '/' + imgPatientName
                patient.imgPatient = imgPatientAdresse

            patient.save()

            # Changement du infopatient
            infopatient.parents_Consanguins = parents_Consanguins
            infopatient.age_maternel_accouchement = age_maternel_accouchement
            infopatient.grossesse_suivi = grossesse_suivi
            infopatient.terme_grossesse = terme_grossesse
            infopatient.precisionTerme = precisionTerme
            infopatient.accouchement_par_voie = accouchement_par_voie
            infopatient.Notion_hospitalisation_age_neonatal = Notion_hospitalisation_age_neonatal
            infopatient.diversification_alimentaire = diversification_alimentaire
            infopatient.souffrance_neonatal = souffrance_neonatal
            infopatient.taille_de_naissance = taille_de_naissance
            infopatient.poids_de_naissance = poids_de_naissance
            infopatient.allaitement = allaitement
            infopatient.retentissement_staturo_ponderale = retentissement_staturo_ponderale

            infopatient.save()
            url = reverse('afficher_patient', args=[patient_id])
            return redirect(url)

        return render(request, 'Administrateur/editer_patient.html', context)
    else:
        return redirect('homPage')

def recherche_patient(request):
    if request.user.is_authenticated:
        error = ""
        errorValue = False
        patients = []
        context = {}

        try:
            patient_bd = Patient.objects.all()
        except BaseException as e:
            error = str(e)
            errorValue = True
        else:
            for p in patient_bd:
                file_name = os.path.basename(p.imgPatient.url)
                img_path = "/imgProfile_patient/" + file_name
                patients.append([p, img_path])

            # --------------Post method----------------------
            if request.method == "POST":
                id = request.POST.get('id')
                nom = request.POST.get('nom')
                mail = request.POST.get('mail')

                query = Q()
                if id:
                    query &= Q(idPatient__contains=id)
                if nom:
                    query &= (Q(nomPatient__icontains=nom) | Q(prenomPatient__icontains=nom))
                if mail:
                    query &= Q(mailPatient__icontains=mail)

                patients = []
                patient_bd = Patient.objects.filter(query)
                for p in patient_bd:
                    file_name = os.path.basename(p.imgPatient.url)
                    img_path = "/imgProfile_patient/" + file_name
                    patients.append([p, img_path])

                context = {
                    'error': error,
                    'errorValue': errorValue,
                    'patients': patients,
                }

        return render(request, "Administrateur/recherchePatients_admin.html", context)
    else:
        return redirect('homPage')

# Creation Admin
def new_admin(request):
    if request.method == "POST":
        formCreation = creationAdmin(request.POST)
        error = False
        context = {"form": formCreation, "error": error}
        if formCreation.is_valid():
            dataConnexion = formCreation.cleaned_data
            usernameAdmin = str(dataConnexion.get('prenomAdmin')) + "_" + str(dataConnexion.get('nomAdmin')) + ".admin"

            # Craetion d'une instance User
            user = User.objects.create_user(username=usernameAdmin,
                                            first_name=dataConnexion.get('prenomAdmin'),
                                            last_name=dataConnexion.get('nomAdmin'),
                                            email=dataConnexion.get('nomAdmin'),
                                            is_admin=True)
            user.set_password(dataConnexion.get('passwordAdmin'))
            if user:
                user.save()
                adminUser = Administrateur(user=user, nomAdmin=dataConnexion.get('nomAdmin'),
                                           prenomAdmin=dataConnexion.get('prenomAdmin'),
                                           passwordAdmin=dataConnexion.get('passwordAdmin'),
                                           mailAdmin=dataConnexion.get('mailAdmin'))
                if adminUser:
                    adminUser.save()
                    return redirect('homPage')
                else:
                    user.delete()

    else:
        formCreation = creationAdmin()
        error = False
        context = {"form": formCreation, "error": error}
    return render(request, "Administrateur/newAdmin.html", context=context)

# Index Admin
def index_admin(request):
    if request.user.is_authenticated:
        error = False
        errorMsg = ""
        patientsNbr = 0
        videosNbr = 0
        rapportsNbr = 0

        # Nbr des attributes
        try:
            specialistesNbr = User.objects.filter(is_pediatre=True).count()
        except User.DoesNotExist:
            specialistesNbr = 0
        else:
            try:
                patientsNbr = len(Patient.objects.all())
                rapportsNbr = len(Actualite.objects.all())
                videosNbr = len(Video.objects.all())
            except BaseException as e:
                print(e)
                error = True
                errorMsg = str(e)
        # Les patients et les pediatres
        try:
            recent_patients = User.objects.filter(is_patient=True).order_by('date_joined')[:20]
            recent_pediatres = User.objects.filter(is_pediatre=True).order_by('date_joined')[:20]
        except BaseException as e:
            error = True
            errorMsg = errorMsg + str(e)
            patients = []
            pediatres = []
        else:
            try:
                patients = []
                pediatres = []
                for p in recent_patients:
                    patient = Patient.objects.get(user=p)
                    file_name = os.path.basename(patient.imgPatient.url)
                    img_path = "/imgProfile_patient/" + file_name
                    patients.append([patient, img_path])

                for p in recent_pediatres:
                    pediatre = Pediatre.objects.get(user=p)
                    pediatres.append(pediatre)
            except BaseException as e:
                error = True
                errorMsg = errorMsg + str(e)

        context = {
            'error': error,
            'errorMsg': errorMsg,
            'specialistesNbr': specialistesNbr,
            'patientsNbr': patientsNbr,
            'rapportsNbr': rapportsNbr,
            'videosNbr': videosNbr,
            'patients': patients,
            'pediatres': pediatres,
        }
        return render(request, "Administrateur/indexAdmin.html", context)
    else:
        return redirect('homPage')

# Deconnexion
def logout_admin(request):
    if request.user.is_authenticated:
        try:
            logout(request)
        except BaseException as e:
            print("Caught exception:", e)
            error = str(e)
            errorValue = True
        return redirect("index_admin")
    else:
        return redirect('homPage')

# Gestion d'administrateur
def gestion_admin(request):
    adminList = Administrateur.objects.all()
    context = {"adminList": adminList}
    return render(request, "Administrateur/gestionAdmin.html", context=context)

def delegationCities_ajax(request):
    selectedValue = request.GET.get('selectedValue', '')
    delegationInstance = Delegation.objects.get(nomDelegation=selectedValue)
    listCities = Ville.objects.filter(delegation=delegationInstance)
    cityNames = listCities.values_list('nomVille', flat=True)
    return JsonResponse({'cityNames': list(cityNames)})


# gestion media

def afficherImg(request):
    if request.user.is_authenticated:
        img = Image.objects.all()
        return render(request, "Administrateur/media/afficherImg.html", {"img": img})
    else:
        return redirect('homPage')


def ajouterImg(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ImageForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('affichage_image')

        else:
            form = ImageForm()
            return render(request, "Administrateur/media/ajouterImg.html", {"form": form})
    else:
        return redirect('homPage')


def modifierImg(request, image_id):
    if request.user.is_authenticated:
        image = get_object_or_404(Image, image_id=image_id)
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES, instance=image)
            if form.is_valid():
                form.save()
                return redirect('affichage_image')
        else:
            form = ImageForm(instance=image)

        return render(request, "Administrateur/media/modifierImg.html", {"form": form})
    else:
        return redirect('homPage')


def supprimerImage(request, image_id):
    if request.user.is_authenticated:
        image = get_object_or_404(Image, image_id=image_id)
        if request.method == 'POST':
            image.delete()
            return redirect('affichage_image')
        else:
            return redirect('affichage_image')
    else:
        return redirect('homPage')


def afficherVideo(request):
    if request.user.is_authenticated:
        video = Video.objects.all()
        return render(request, "Administrateur/media/afficherVideo.html", {"video": video})
    else:
        return redirect('homPage')


def ajouterVideo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = VideoForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('affichage_video')
            else:
                return redirect('affichage_video')
        else:
            form = VideoForm()
            return render(request, "Administrateur/media/ajouterVideo.html", {"form": form})
    else:
        return redirect('homPage')


def modifierVideo(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, video_id=video_id)
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES, instance=video)
            if form.is_valid():
                form.save()
                return redirect('affichage_video')
        else:
            form = VideoForm(instance=video)

        return render(request, "Administrateur/media/modifierVideo.html", {"form": form})
    else:
        return redirect('homPage')


def supprimerVideo(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, video_id=video_id)
        if request.method == 'POST':
            video.delete()
            return redirect('affichage_video')
        else:
            return redirect('affichage_video')
    else:
        return redirect('homPage')


# gestion news

def afficherActualite(request):
    if request.user.is_authenticated:
        actualite = Actualite.objects.all()
        return render(request, "Administrateur/news/show_news.html", {"actualite": actualite})
    else:
        return redirect('homPage')



def ajouterActualite(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ActualiteForm(data=request.POST, files=request.FILES)
            form.fields['pdf'].required = False
            if form.is_valid():
                form.save()
                return redirect('affichage_actualite')

        else:
            form = ActualiteForm()
            return render(request, "Administrateur/news/add_news.html", {"form": form})
    else:
        return redirect('homPage')



def supprimerActualite(request, actualite_id):
    if request.user.is_authenticated:
        actualite = get_object_or_404(Actualite, actualite_id=actualite_id)
        if request.method == 'POST':
            actualite.delete()
            return redirect('affichage_actualite')
        else:
            return redirect('affichage_actualite')
    else:
        return redirect('homPage')


def modifierActualite(request, actualite_id):
    if request.user.is_authenticated:
        actualite = get_object_or_404(Actualite, actualite_id=actualite_id)
        if request.method == "POST":
            form = ActualiteForm(request.POST, request.FILES, instance=actualite)
            if form.is_valid():
                form.save()
                return redirect('affichage_actualite')
        else:
            form = ActualiteForm(instance=actualite)

        return render(request, "Administrateur/news/edit_news.html", {"form": form})
    else:
        return redirect('homPage')
