"""
Configuration des URLs pour l'application 'account' de notre site

Ce module associe chaque URL à une fonction de vue spécifique.
"""

from django.urls import path
from . import views

from django.urls import path, re_path, include

#Défini le nom de l'application, que  l'on utilisera donc dans "siteCourse"
app_name = "accounts"

urlpatterns = [
#ici on écrit par dessus les urls de allauth
    # Page d'accueil, redirige vers la vue 'account'
    path('', views.account , name='home'),

    # Page de suppresion de compte
    path('delete/', views.delete_account, name='delete_account'),

    # Active la suppression d'un compte social, sans passé par une page intermédiaire
    path('delete_social/', views.delete_social_account, name='delete_social_account'),

    # Page de changement d'email
    path('change_email/', views.change_email, name='change_email'),

    # Page de changement de mot de passe
    path('change_password/', views.change_password, name='change_password'),

    # Page de connexion, redirige vers la vue 'login_user'
    path('login/', views.login_user , name='login'),

    # Page d'inscription, redirige vers la vue 'register_user'
    path('signup/', views.register_user , name='signup'),

    # Page de déconnexion, redirige vers la vue 'logout_user'
    path('logout/', views.logout_user , name='logout'),

    #Chemin pour l'activation de comptes
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

    #Chemin pour la page qui sert a renvoyer un nouveau lien
    path('validation_link_sender/', views.validation_link_sender, name='validation_link_sender'),

    #Lien utilisé pour erreurs de création compte avec google, si l'email est déja use par compte utilisateur
    path('3rdparty/signup/', views.error_google_creation, name="error_google_creation"),

    #Lien pour le reset du mots de passe
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.passwordResetConfirm, name='password_reset_confirm'),

    #Lien pour la validation changement d'email
    path('email_change/<uidb64>/<token>/', views.emailChangeConfirm, name='email_change_confirm'),

    # TODO : Ajouter d'autres URL si nécessaire
    #path('mdpchange,.../......) etc
]