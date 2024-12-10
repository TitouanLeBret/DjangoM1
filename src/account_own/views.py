from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
#Pour la modification du mot de passe
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
#Q permet de faire des requetes plus complexe
from django.db.models import Q
from inscriptions.models import InscriptionCourse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
#Import de tous nos formulaires
from .forms import *


#Utilisation du modèle d'utilisateur personnalisé (custom user), définis dans l'app custom_user dans models.py
#Ce custom user vient du module Django django_use_email_as_username
User = get_user_model()



"""***********************************************************


**************** PARTIE CONNEXION A UN COMTPE ****************


***********************************************************"""



#Fonction pour la vue de login

#Si la requete est de type POST
    #Verifie que l'utilisateur existe et le connecte si c'est le cas
    #Sinon renvoie une erreur dans le formulaire
#S'il n'y a pas de requete
    #Renvoie un formulaire de base AuthenticationFormCaptcha()
    #PS : ce formulaire AuthenticationForm prend automatiquement en compte notre custom_user et a donc un champs email et password

def login_user(request):
    if request.user.is_authenticated :
        return redirect("accounts:home")
    if request.method=="POST" :
        form = AuthenticationFormCaptcha(data=request.POST)
        if form.is_valid():
            username = request.POST['username']  # email
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            #On peut connecter le user sans risque qu'il n'existe pas car AuthenticationForm vérifie qu'il existe et qu'il soit actif
            login(request, user)
            return redirect('accueil')
        else :
            messages.error(request, 'Captcha incorrect ou mauvais identifiant/mot de passe')
    form = AuthenticationFormCaptcha()
    return render(request, 'accounts/login.html', {'form': form})





"""***********************************************************


**************** PARTIE DECONNEXION DU COMTPE ****************


***********************************************************"""







#Fonction de déconnexion
#Déconnecte l'utilisateur et renvoie vers l'accueil

#A FAIRE PEUT ETRE :
    #Vérifier que l'utilisateur est connecté
    #Tester ce qu'il se passe sinon
def logout_user(request):
    logout(request)
    return redirect('accueil')






"""***********************************************************


**************** PARTIE CREATION DU COMPTE ****************


***********************************************************"""



#Fonction pour la vue de register

#Si la requete est de type POST
    #Test si le formulaire est valide
    #--> la fonction is_valid() viens de Django, et comme nous avons définis champs email et password
    #--> vérifie donc email valide (présence d'un '@' et d'un '.')
    #--> vérifie que les 2 mots de passe correspondent et qu'ils respectent les règles de sécurités (8 carac, pas mdp courant, pas entierement numérique, pas trop semblable a infos perso (email))
#S'il n'y a pas de requete
    #Renvoie un formulaire EmailUserCreationForm() (structure que l'on a définis plus haut)

#La partie vérification mail a était réaliser grace au tutoriel : https://www.youtube.com/watch?v=wB1qOExDsYY

def activate_account(request, uidb64, token): #uidb64 = représentation en base 64
    try :
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except :
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé avec succès')
        return redirect('accounts:login')
    else :
        messages.error(request,'Ce lien d\'activation est invalide ou à expiré')
    return redirect('accueil')

def activateEmail(request,user,email):
    mail_subject = "Activer votre compte."
    #Potentiellemenet a supprimer (4 lignes en dessous)
    if get_current_site(request).domain=="localhost" :
        domain = "127.0.0.1"
    else :
        domain = get_current_site(request).domain
    message = render_to_string('email/activation_mail.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure else 'http',
    })
    mail_message = EmailMessage(mail_subject, message, to=[email])
    if mail_message.send():
        messages.success(request,f'Un lien de vérification viens de vous être envoyer par mail à l\'adresse {email}. \
        Attention, ce mail est valide durant 30 minutes')
    else :
        messages.error(request, f'Il y\'a eu un problème pendant l\'envois du mail de vérification à l\'email :{email}, vérifiez si celle-ci est correcte')


def register_user(request):
    if request.user.is_authenticated :
        return redirect("accounts:home")
    if request.method == "POST":
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_social_account = False
            user.save()
            #login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            activateEmail(request,user,form.cleaned_data['email'])
            #Peut etre ici faire une vérif pour si activateEmail ne s'envoie pas on supprime le user ?????
            return redirect("accounts:login")

    else :
        form = EmailUserCreationForm()
    return render (request, 'accounts/signup.html', {'form': form})

#Erreur si on essaye de créer un compte avec google mais que l'email du compte google est déja utilisé
def error_google_creation(request):
    messages.error(request,"L'email de votre compte google est déja utilisé par un compte utilisateur")
    return redirect('accounts:login')



#Fonction pour le renvoie de lien de vérification

def validation_link_sender(request):
    if request.method == 'POST':
        form = SendEmailValidForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try :
                user = User.objects.get(email=email)

            except User.DoesNotExist :
                messages.error(request,'Aucun compte avec cette adresse mail n\'existe')
                #Pas sécuriser d'indiquer ça, il faut le retirer, mais c'est pratique pendant la prod, pour savoir les comptes qui existes quand on test
                return redirect("accounts:login")

            if user.is_active:
                messages.error(request,"Cet utilisateur est déjà activé.")
                return redirect("accounts:login")


            # Génération du lien de validation
            activateEmail(request,user,form.cleaned_data['email'])
            return redirect("accounts:login")
    else:
        form = SendEmailValidForm()

    return render(request, 'accounts/send_email_verif.html', {'form': form})




"""**************************************************************************************


******** PARTIE AFFICHAGE DE LA VU DU COMPTE ET MODIFS INFO (NOM,PRENOM,AGE,...) ********


**************************************************************************************"""



#Fonction pour la vue du compte

#Permet à l'utilisateur de visualiser et de modifier ses informations personnelles, telles que son prénom, nom et âge.
#- Si une requête POST est envoyée :
    #- Vérifie la validité des données soumises via un formulaire.
    #- Si valide, met à jour les informations de l'utilisateur dans la base de données.
    #- Si invalide, affiche les erreurs et réinitialise le formulaire.
#- Si aucune requête POST :
    #- Pré-remplit les champs avec les données actuelles de l'utilisateur s'il est connecté.
    #- Affiche la page sans formulaire si l'utilisateur n'est pas connecté

def account(request):
    if request.user.is_authenticated:
        # Traitement du formulaire lorsqu'une qu'il est soumis (requete POST)
        if request.method == "POST":
            form = AccountForm(request.POST) # Création du formulaire avec les données soumises
            if form.is_valid(): # Vérification de la validité des données soumises
                user = request.user
                user.prenom = form.cleaned_data.get('prenom')
                user.nom = form.cleaned_data.get('nom')
                user.age = form.cleaned_data.get('age')
                # Enregistre les modifications dans la base de données
                user.save()
                messages.success(request,"Modifactions validées")
                return render(request, 'accounts/accounts.html', {'form': form})
            else:
                # Si le formulaire est invalide, on renvoie la page d'accueil avec les erreurs du formulaire
                # Ce cas n'arrive jamais je penses, car le POST n'est effectué que si les données sont valides
                # Mais laisser pour sécurité maximum ?
                return render(request, 'accounts/accounts.html', {'form': form })
        else:
            # Si pas de soumission POST, on créer formulaire vierge et on affiche la page
            initial_data = {
                'prenom': request.user.prenom,
                'nom': request.user.nom,
                'age': request.user.age,
            }  # Rempli avec les données de l'utilisateur connecté
            form = AccountForm(initial=initial_data)
            return render(request, 'accounts/accounts.html', {'form': form})
    else :
        return login_user(request)





"""*************************************************************


**************** PARTIE SUPPRESION DU COMPTE ****************


*************************************************************"""



#Fonction pour la suppression de compte

#Permet à l'utilisateur de supprimer définitivement son compte après vérification de son email et de son mot de passe.
#- Si une requête POST est envoyée :
    #- Vérifie les identifiants soumis (email et mot de passe) via un formulaire.
    #- Si valide, supprime l'utilisateur de la base de données et affiche un message de confirmation.
    #- Si invalide, affiche un message d'erreur.
#- Si aucune requête POST :
    #- Affiche un formulaire de suppression de compte.

def delete_account(request):
    if not request.user.is_authenticated :
        return redirect("accounts:home")
    if request.method == "POST":
        form = UserDeleteAccountForm(request.user,request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)
            if user:
                # Supprimer les inscriptions associées à l'id de l'utilisateur
                InscriptionCourse.objects.filter(user_id=user.id).delete()

                user.delete()
                messages.success(request, "Votre compte a été supprimé avec succès.")
                return redirect('account_login')  # Rediriger vers la page de connexion
        else:
            messages.error(request, "Les informations saisies sont incorrectes ou ne correspondent pas a votre compte.")
    else :
        form = UserDeleteAccountForm(request.user)
    return render(request, 'accounts/delete_account.html', {'form': form})



#Même principe qu'au dessus, mais pas de vérifications ici, car si on demande a l'user de se reconnecter a son comtpe social,
#il est la plupart du temps enregistré, donc pas d'intérêt
def delete_social_account(request):
    if not request.user.is_authenticated :
        return redirect("accounts:home")
    if request.user.is_authenticated :
        if request.user.is_social_account :
            user = request.user
            # Supprimer les inscriptions associées à l'id de l'utilisateur
            InscriptionCourse.objects.filter(user_id=user.id).delete()
            user.delete()
            messages.success(request, "Votre compte a été supprimé avec succès.")
            return redirect('account_login')  # Rediriger vers la page de connexion
        else :
            return redirect('/accounts')
    else :
        return redirect('account_login') # Rediriger vers la page de connexion

"""***********************************************************


**************** PARTIE CHANGEMENT DE L'EMAIL ****************


***********************************************************"""


#Fonction pour le changement d'email d'un compte

#Permet à l'utilisateur de modifier son adresse email après vérification de l'ancien email et du mot de passe.
#- Si une requête POST est envoyée :
    #- Vérifie les données via un formulaire.
    #- Si valide, met à jour l'email de l'utilisateur dans la base de données et affiche un message de confirmation.
    #- Si invalide, affiche un message d'erreur.
#- Si aucune requête POST :
    #- Affiche un formulaire pour le changement d'email.

def change_email(request):
    if not request.user.is_authenticated :
        return redirect("accounts:home")
    if request.method == "POST":
        form = UserChangeMailForm(request.user,request.POST)
        if form.is_valid():
            old_email = form.cleaned_data.get("old_email")
            password = form.cleaned_data.get("password")
            new_email = form.cleaned_data.get("new_email")
            user = authenticate(request, email=old_email, password=password)
            if user:
                user.temp_email = new_email #on stocke la nouvelle adresse potentielle
                user.save()
                mail_subject = "Changement d'email."
                # Potentiellemenet a supprimer (4 lignes en dessous)
                if get_current_site(request).domain == "localhost":
                    domain = "127.0.0.1:8000"
                else:
                    domain = get_current_site(request).domain
                message = render_to_string('email/email_change.html', {
                    'user': user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure else 'http',
                })
                mail_message = EmailMessage(mail_subject, message, to=[new_email])
                if mail_message.send():
                    messages.success(request,
                                     f'Un lien de validation viens de vous être envoyer par mail à l\'adresse {new_email}. \
                                    Attention, ce mail est valide durant 30 minutes')
                else:
                    messages.error(request,
                                   f'Il y\'a eu un problème pendant l\'envois du mail de vérification à l\'email :{new_email}, vérifiez si celle-ci est correcte')
                return redirect('accounts:home')
            else:
                messages.error(request, "Les informations saisies sont incorrectes.")
    else :
        form = UserChangeMailForm(request.user)
    return render(request, 'accounts/change_email.html', {'form': form})


#Fonction pour valider le changemnet d'adresse mail :
def emailChangeConfirm(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        new_email = user.temp_email
        if new_email:
            user.email = new_email
            user.temp_email = None
            user.save()
            messages.success(request,"Votre mail a était mis à jour")
        else :
            messages.error(request,"Il y'a une erreur avec votre addresse mail") #N'arrive logiquement jamais car pour arriver sur cette page, il faut cliquer sur le lien sur la dite addresse mail, qui est donc obligatoirement valide
        return redirect('accounts:home')
    else:
        messages.error(request, "Le lien de validation est invalide ou expiré.")
        return redirect('accounts:home')


"""***********************************************************


************* PARTIE CHANGEMENT DU MOT DE PASSE **************


***********************************************************"""





#Fonction pour le changement de mot de passe d'un compte

#Permet à l'utilisateur de modifier son mot de passe après vérification de l'ancien mot de passe.
#- Si une requête POST est envoyée :
    #- Vérifie les données via un formulaire.
    #- Si valide :
        #verifie que le mot de passe respecte les regles de sécurité django : validate_password()
            #si oui : met à jour le mot de passe de l'utilisateur dans la base de données, reconnecte l'utilisateur et affiche un message de confirmation.
            #si non : renvoie sur la page de base avec la les messages d'erreur renvoyé par la fonction validate_password (1 ou plusieurs messages)
    #- Si invalide, affiche un message d'erreur.
#- Si aucune requête POST :
    #- Affiche un formulaire pour le changement de mot de passe.

def change_password(request):
    if not request.user.is_authenticated :
        return redirect("accounts:home")
    if request.method == "POST":
        form = UserChangePasswordForm(request.user,request.POST)
        if form.is_valid():
            email = request.user.email
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password1')

            user = authenticate(request, email=email, password=old_password)
            if user:
                try:
                    # Valider le nouveau mot de passe avec les règles de Django
                    validate_password(new_password, user=user)
                    
                    # Si valide, enregistrer le nouveau mot de passe
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Votre mot de passe a été changé.")

                    # Reconnexion automatique
                    login(request, user)
                    return redirect('accounts:home')
                # Si le nouveau mot de passe ne respecte pas les règles de Django 
                except ValidationError as e:
                    #On parcours toutes les erreurs pour les ajouter et que l'utilisateur voit quelle regles il ne respecte pas
                    for error in e:
                        messages.error(request, error) #exemple d'erreur : mot de passe trop court, trop courant, entierement numérique
            else:
                messages.error(request, "L'ancien mot de passe est incorrect.")
    else:
        form = UserChangePasswordForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})



#Cette partie est pour la réinitialisation du mot de passe par mail

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            associated_user = User.objects.filter(Q(email = user_email)).first()
            if associated_user:
                mail_subject = "Réinitialiser votre mot de passe."
                # Potentiellemenet a supprimer (4 lignes en dessous)
                if get_current_site(request).domain == "localhost":
                    domain = "127.0.0.1:8000"
                else:
                    domain = get_current_site(request).domain
                print(domain)
                message = render_to_string('email/reinitialise_mot_de_passe.html', {
                    'user': associated_user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.id)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure else 'http',
                })
                mail_message = EmailMessage(mail_subject, message, to=[user_email])
                if mail_message.send():
                    messages.success(request,
                                     f'Un lien de réinitialisation viens de vous être envoyer par mail à l\'adresse {user_email}. \
                    Attention, ce mail est valide durant 30 minutes')
                else:
                    messages.error(request,
                                   f'Il y\'a eu un problème pendant l\'envois du mail de vérification à l\'email :{user_email}, vérifiez si celle-ci est correcte')
                return redirect('accounts:home')
            else:
                messages.error(request, "L'email que vous avez rentré n'est pas valide")
        else :
            messages.error(request,"Vous n'avez pas complété le captcha")
    form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})


def passwordResetConfirm(request,uidb64,token): # uidb64 = représentation en base 64
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordFormCaptcha(user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre mot de passe a était changé avec succès ')
                return redirect('accounts:login')
            else :
                #gestion de l'affichage des erreurs
                if 'captcha' in form.errors:
                    messages.error(request, "Veuillez remplir le ReCaptcha.")

                password_errors = []
                if 'new_password1' in form.errors:
                    for error in form.errors['new_password1']:
                        password_errors.append(f"Mot de passe : {error}")
                if 'new_password2' in form.errors:
                    for error in form.errors['new_password2']:
                        password_errors.append(f"Mot de passe (confirmation) : {error}")

                if password_errors:
                    messages.error(request, " ".join(password_errors))

        form = SetPasswordFormCaptcha(user)
        return render(request, 'accounts/password_reset.html', {'form': form})
    else:
        messages.error(request, 'Ce lien de réinitialisation est invalide ou à expiré')
    messages.error(request, "Une erreur est survenue, vous allez etre redirigé vers la page de connexion")
    return redirect('accounts:home')


