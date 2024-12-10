import hashlib
import os

from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import InscriptionCourse, CertificatMedical

"""
Formulaire pour l'inscription a une course
"""
class InscriptionForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())  # Champ supplémentaire non lié au modèle

    class Meta:
        model = InscriptionCourse
        fields = ['nom', 'prenom', 'age', 'course', 'certificat_med']
        widgets = {
            'certificat_med': forms.FileInput(attrs={'accept': '.pdf'}),
        }
