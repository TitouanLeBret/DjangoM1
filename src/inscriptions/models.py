import os

from django.db import models
from django.contrib.auth import get_user_model
from private_storage.fields import PrivateFileField
from django.conf import settings

User = get_user_model()

class CertificatMedical(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    certificat_med_name = models.CharField(max_length=2048,blank=True,null=True)

# Modèle représentant une inscription à une course.
class InscriptionCourse(models.Model):
    """
       Ce modèle stocke les informations relatives à l'inscription d'un participant à une course.
    """
    CHOICES_COURSE = [
        ('5km', '5 km'),
        ('10km', '10 km'),
        ('semi-marathon', 'Semi-marathon'),
        ('marathon', 'Marathon'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    age = models.IntegerField()
    course = models.CharField(max_length=255, choices=CHOICES_COURSE)
    # Certificat médical :
    certificat_med = PrivateFileField(upload_to='certificats_medicaux/',blank=False, default=False)

    # Statut de l'inscription (complète ou non)
    inscription_complete = models.BooleanField(default=False)
    # Date de l'inscription, ajoutée automatiquement à la création de l'objet
    inscription_date = models.DateField(auto_now_add=True)

    #paiement_complet = models.BooleanField()
    #compte = models.ForeignKey('InscriptionCompte', null=False, on_delete=models.CASCADE)

    #variable sur le paiement
    #facture
    invoice = models.CharField(max_length=255, null=True, blank=True)
    #payé vrai ou faux
    paid = models.BooleanField(default=False)

    """
        Fonction pour l'affichage d'une Inscription (Utile pour le débug)
    """
    def __str__(self):
        status = "Complète" if self.inscription_complete else "Incomplète"
        return f"Inscription: {self.prenom} {self.nom} ({self.age} ans) - Course: {self.course} - Statut: {status} "


    """
        Définis le nom de la table dans notre base de donnée
    """
    class Meta:
        db_table = "InscriptionCourse"  # Nom exact de la table dans la base de données
