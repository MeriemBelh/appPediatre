from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
#from Administrateur.models import Patient

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

""""
class PatientForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Patient
        fields = [
            'nomPatient', 'prenomPatient', 'numTelephoneMere',
            'numTelephonePere', 'adressePatient', 'delegationPatient', 'villePatient',
            'dateNaissancePatient', 'couvertureMedical', 'mailPatient',
        ]
"""