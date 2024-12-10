from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models

"""
Fichier générer automatiquement par python manage.py create_custom_user_app
Voir doc : https://pypi.org/project/django-use-email-as-username/
"""
class User(BaseUser):
    prenom = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    is_social_account = models.BooleanField(default=True)
    temp_email = models.EmailField(null=True, blank=True) # champs pour le changement d'email, qui stocke la potentielle nouvelle addresse
    objects = BaseUserManager()

    def __str__(self):
        return str(self.email) + " | " + str(self.prenom) + " | " + str(self.nom) + " | " + str(self.age)