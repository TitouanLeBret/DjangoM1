"""
Django settings for siteCourse project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
from django.conf.global_settings import CSRF_TRUSTED_ORIGINS
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="fallback-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#urls pour Ngrok permet de mettre le site en https pour les tests avec paypal, à changer à chaque session
ALLOWED_HOSTS = ['127.0.0.1','5b59-46-193-2-97.ngrok-free.app','djangom1.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://5b59-46-193-2-97.ngrok-free.app','https://djangom1.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',

    #Pour auth par email :
    'django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig',
    #'account.apps.CustomUserConfig',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'account_own',
    'inscriptions',

    #Pour les captchas
    'django_recaptcha',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    #paypal library
    'paypal.standard.ipn',

    'private_storage'
]

# requis par django-allauth
SITE_ID = 1


CRISPY_TEMPLATE_PACK = 'bootstrap4'
# URL où rediriger après la connexion/déconnexion
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_AUTO_SIGNUP = True

#Permet de passer directement a la vue de connexion pour le social account, sans passer par une page intermediaire
SOCIALACCOUNT_LOGIN_ON_GET = True

# Configuration de l'authentification
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Authentification Django classique
    'allauth.account.auth_backends.AuthenticationBackend',  # Authentification sociale
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'titouanlebretuniv@gmail.com'
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="") #Mot de passe d'application
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Durée de vie du token de vérification -> sera utilisé pour vérifer que le temps actuel n'est pas différent de plus de
# 1800 secondes (30 min) du temps a laquelle le token de validation par mail a était crée
PASSWORD_RESET_TIMEOUT = 1800


ACCOUNT_EMAIL_REQUIRED = True  # Pour s'assurer que l'email est requis
SOCIALACCOUNT_EMAIL_REQUIRED = True  # Pour rendre l'email obligatoire lors de la connexion via Google
SOCIALACCOUNT_QUERY_EMAIL = True  # Pour s'assurer que l'email est demandé lors de l'inscription

#Désactive les mecanismes de base de allauth car on le gere nous meme
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Ne pas envoyer de mail de vérification automatique
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # Pas de vérification de l'email lors de la connexion sociale

#Pour la liste des providers et leurs settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
    }
}

#Pour les captcah GOOGLE :
#NE PAS LES LAISSER LA, NOUS DEVONS LES IMPORT
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="")


AUTH_USER_MODEL = 'account_own.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #Pour Oauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'siteCourse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "siteCourse/templates"),
            os.path.join(BASE_DIR, "inscriptions/templates"),
            os.path.join(BASE_DIR, "account_own/templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'siteCourse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'DBProjetSite.sqlite3',
    }
}"""

#Gestion DB avec PostgreSQL
import dj_database_url

DATABASES = {

    'default' : dj_database_url.parse(config("POSTGRES_URL", default=""))

}





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'Fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Pour gestion des sessions de connexion
# Durée de vie de la session en secondes (6 heures ici)
SESSION_COOKIE_AGE = 6 * 60 * 60  # 6 heures

# Session expire si le nav se ferme
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#ajout parametre paypal
#set sandbox to true
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'business@etu.unicaen.fr' #Business sandBox account


#Stockage des pdf de certificats médicaux
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Spécifiez le dossier de base pour les fichiers privés
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'private_storage')

# URL d'accès aux fichiers privés (note : ce n'est pas l'URL par défaut)
PRIVATE_STORAGE_URL = '/private-media/'

PRIVATE_STORAGE_FILE_OVERWRITE = False  # Pour ne pas écraser les fichiers existants

# Configurez le stockage privé pour qu'il soit utilisé par le modèle
DEFAULT_FILE_STORAGE = 'private_storage.storage.PrivateFileSystemStorage'
PRIVATE_STORAGE_AUTH_FUNCTION = 'siteCourse.permissions.custom_access_function'
"""ATTENTION, CHANGER LA PERMISSION POUR QUE CE SOIT UNIQUEMENT LE PROPRIO DU PDF ET LES ADMINS"""