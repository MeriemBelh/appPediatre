from django import forms
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


class connexionAdmin(forms.Form):
    login = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)


class creationAdmin(forms.Form):
    nomAdmin = forms.CharField(widget=forms.TextInput)
    prenomAdmin = forms.CharField(widget=forms.TextInput)
    passwordAdmin = forms.CharField(widget=forms.TextInput)
    mailAdmin = forms.CharField(widget=forms.EmailInput)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image_id", "image")


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("video_id", "titre", "description", "lien")


class ActualiteForm(forms.ModelForm):
    class Meta:
        model = Actualite
        fields = ("actualite_id", "titre", "texte", "auteur", "pdf")