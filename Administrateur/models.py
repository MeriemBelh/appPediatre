from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from datetime import datetime

from Patient.models import *
from Pediatre.models import *


class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #idAdmin = models.AutoField(primary_key=True)
    nomAdmin = models.CharField(max_length=60)
    prenomAdmin = models.CharField(max_length=60)
    passwordAdmin = models.CharField(max_length=60)
    mailAdmin = models.EmailField(unique=True)

    def __str__(self):
        return self.prenomAdmin + " " + self.nomAdmin


class Conversation(models.Model):
    idConversation = models.AutoField(primary_key=True)
    sujet = models.CharField(max_length=300, default="No Subject")
    receiver =  models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='received_conversation')
    sender =  models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sent_conversation')
    dateStart =  models.CharField(max_length=100,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dateUpdated = models.CharField(max_length=100, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    nbrMessage = models.IntegerField(default=1)

    def __str__(self):
        return str(self.dateStart) + "-" + str(self.sender) + "-" + str(self.receiver)


class Message(models.Model):
    idMessage = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='received_messages')
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sent_messages')
    dateEnvoie = models.CharField(max_length=100,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    vu = models.BooleanField(default=False)
    message = models.TextField()

    def __str__(self):
        return str(self.idMessage)


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    lien = models.CharField(max_length=255, unique=True)


class Actualite(models.Model):
    actualite_id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=120)
    post_date = models.DateTimeField(auto_now_add=True)
    texte = models.TextField()
    auteur = models.CharField(max_length=40)
    pdf = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(['pdf'])], null=True)


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="imgGalerie/")
