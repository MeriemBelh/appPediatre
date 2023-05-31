import os

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from Patient.models import *
from Pediatre.models import *
from Patient.views import *
from Pediatre.views import *

from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        if request.user.is_pediatre:
            return redirect("home_pediatre")
        elif request.user.is_patient:
            return redirect("home_patient")
        else:
            return redirect('index_admin')
    else:
        actualite = Actualite.objects.order_by('-post_date')[:8]
        return render(request, "homePage.html", {'actualite': actualite})


def loginUsers(request):
    error = ""
    errorValue = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        is_user = request.POST['is_user']
        user = authenticate(username=username, password=password)
        if (is_user == 'is_pediatre'):
            if user is not None and user.is_pediatre:
                login(request, user)
                return redirect('home_pediatre')
            else:
                error = 'L\'identifiant ou le mot de passe que vous avez saisi n’est pas associé à un compte pédiatre!'
                errorValue = True
        elif (is_user == 'is_patient'):
            if user is not None and user.is_patient:
                login(request, user)
                return redirect('home_patient')
            else:
                error = 'L\'identifiant ou le mot de passe que vous avez saisi n’est pas associé à un compte patient!'
                errorValue = True
        elif (is_user == 'is_admin'):
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('index_admin')
            else:
                error = 'L\'identifiant ou le mot de passe que vous avez saisi n’est pas associé à un compte admin!'
                errorValue = True
    return render(request, 'loginUsers.html', {'error': error, 'errorValue': errorValue})


def image(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        img = Image.objects.all()

        context = {
            'patient': patient,
            'imgPatient': img_path,
            "img": img,
        }
        return render(request, "image.html", context)
    else:
        img = Image.objects.all()
        return render(request, "image.html", {"img": img})


def video(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        video_ = Video.objects.all()
        context = {
            'patient': patient,
            'imgPatient': img_path,
            "video": video_,
        }
        return render(request, "video.html", context)
    else:
        video_ = Video.objects.all()
        return render(request, "video.html",{"video": video_})


def about(request):
    return render(request, "about.html")


def actualites(request):
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user=request.user)
        except Exception as e:
            patient = None
            print('Exception: ', e)
        file_name = os.path.basename(patient.imgPatient.url)
        img_path = "/imgProfile_patient/" + file_name
        actualite = Actualite.objects.all()

        context = {
            'patient': patient,
            'imgPatient': img_path,
            "actualite": actualite,
        }
        return render(request, "actualites.html", context)
    else:
        actualite = Actualite.objects.all()
        return render(request, "actualites.html",{"actualite": actualite})


def actualite(request, actualite_id):
    actualite = get_object_or_404(Actualite, actualite_id=actualite_id)
    return render(request, "actualite.html",{"actualite": actualite})