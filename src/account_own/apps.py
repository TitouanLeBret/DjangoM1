from django.apps import AppConfig

"""
Fichier générer automatiquement par python manage.py create_custom_user_app
Voir doc : https://pypi.org/project/django-use-email-as-username/
"""

class CustomUserConfig(AppConfig):
    name = 'account_own'
    verbose_name = 'Custom user management application'
