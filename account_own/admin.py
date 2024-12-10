from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin

from .models import User

"""
Fichier générer automatiquement par python manage.py create_custom_user_app
Voir doc : https://pypi.org/project/django-use-email-as-username/
"""

admin.site.register(User, BaseUserAdmin)
