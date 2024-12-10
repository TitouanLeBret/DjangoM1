from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model
#Pour le captcha
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox



#Utilisation du modèle d'utilisateur personnalisé (custom user), définis dans l'app custom_user dans models.py
#Ce custom user vient du module Django django_use_email_as_username
User = get_user_model()




# personnaliser de connexion (on se ressert de celui fournis mais on lui ajoute un captcha)

#-Champs 1 et 2, champs de base de AuthenticationForm
#-Captcha
class AuthenticationFormCaptcha(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())




#Formulaire personnaliser de création de compte utilisateur avec email
#Ce formulaire est une modification d'un formulaire django

#-Champs 1 : Email
#-Champs 2 : Mot de passe
#-Champs 3 : Verification mot de passe
class EmailUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # Utilisation de l'email et des mots de passe

    #Renome le champs email en "Email", de base s'appelle "Adresse électronique"
    email = forms.EmailField(label='Email', max_length=254)  # Champ pour l'email



#Partie pour le renvoie d'un mail de vérification
class SendEmailValidForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email





#Création de notre formulaire de modification de compte
#Il faut ajotuer :
# -modification mots de passe
# -gérer ajout certif med et modifs de celui-ci (on peut le consulter)
# -modifs de l'email (doit donc modifier la connexion au compte)
# -autres modifs ??????
class AccountForm(forms.Form):
    # Définition des champs du formulaire d'inscription
    prenom = forms.CharField(max_length=100, required=False)
    nom = forms.CharField(max_length=100, required=False)
    #email = forms.EmailField()
    age = forms.IntegerField(min_value=1, max_value=110, required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



#Formulaire personnaliser de changement d'email
#Ce formulaire est une modification d'un formulaire django

#-Champs 1 : Email
#-Champs 2 : Mot de passe

#La fonction __init__ intialise un formulaire mais en lui donnant un user, pour permettre les vérifications nécessaire plus tard
class UserDeleteAccountForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

#Explication de pourquoi *args et **kwargs sur stackoverflow : https://stackoverflow.com/questions/871037/django-overriding-init-for-custom-forms
    def __init__(self, user ,*args, **kwargs):
        self.user = user #Donner l'utilisateur actif
        super().__init__(*args, **kwargs)

# Fonction clean_xxx appelé automatiquement par django lors de is_valid()
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.user.email:
            raise forms.ValidationError("L'email ne correspond pas.")
        return email







#Formulaire personnaliser de changement d'email
#Ce formulaire est une modification d'un formulaire django

#-Champs 1 : Ancien Email
#-Champs 2 : Mot de passe
#-Champs 3 : Nouvel email

#La fonction __init__ intialise un formulaire mais en lui donnant un user, pour permettre les vérifications nécessaire plus tard
class UserChangeMailForm(forms.Form):
    old_email = forms.EmailField(label='Ancien Email', max_length=254)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    new_email = forms.EmailField(label='Nouvel Email', max_length=254)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

#Explication de pourquoi *args et **kwargs sur stackoverflow : https://stackoverflow.com/questions/871037/django-overriding-init-for-custom-forms
    def __init__(self, user ,*args, **kwargs):
        self.user = user  #Donner l'utilisateur actif
        super().__init__(*args, **kwargs)


#Fonction clean_xxx appelé automatiquement par django lors de is_valid()
    def clean_old_email(self):
        old_email = self.cleaned_data.get('old_email')
        if old_email != self.user.email:
            raise forms.ValidationError("L'ancien email ne correspond pas à celui associé à votre compte.")
        return old_email

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return new_email






#Formulaire personnaliser de changement de mot de passe
#Ce formulaire est une modification d'un formulaire django

#-Champs 1 : Email
#-Champs 2 : Mot de passe actuel
#-Champs 3 : Nouveau Mot de passe
#La fonction __init__ intialise un formulaire mais en lui donnant un user, pour permettre les vérifications nécessaire plus tard
class UserChangePasswordForm(SetPasswordForm):
    #on veut quand même vérifier l'ancien mot de passe
    old_password = forms.CharField(label='Ancien mot de passe', widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

#Formulaire pour envoie la demande pour réinitialiser le mot de passe
class PasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm,self).__init__(*args, **kwargs)


#Formulaire pour réinitialiser le mot de passe
class SetPasswordFormCaptcha(SetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']