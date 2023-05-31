from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_pediatre', True)
        extra_fields.setdefault('is_patient', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_pediatre') is not True:
            raise ValueError('Superuser must have is_pediatre=True.')
        if extra_fields.get('is_patient') is not True:
            raise ValueError('Superuser must have is_patient=True.')

        return self.create_user(username, email, password, **extra_fields)
        
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_pediatre = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def __str__(self):
        return self.username


class Pediatre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #idPediatre = models.AutoField(default=timezone.now)
    inpe = models.IntegerField(unique=True)
    cniPediatre = models.CharField(max_length=8)
    nomPediatre = models.CharField(max_length=60)
    prenomPediatre = models.CharField(max_length=60)
    mailPediatre = models.CharField(max_length=120, unique=True)
    numTelephonePediatre = models.BigIntegerField(unique=True)
    adressePediatre = models.TextField(max_length=300)
    passwordPediatre = models.CharField(max_length=60)
    hopitalPediatre = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.nomPediatre + " " + self.prenomPediatre