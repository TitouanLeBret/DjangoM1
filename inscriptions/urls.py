from django.urls import path, include
from . import views
#from siteCourse.views import inscriptions


#Défini le nom de l'application, que  l'on utilisera donc dans "siteCourse"
app_name = "inscriptions"

urlpatterns = [
    # Page d'accueil, redirige vers la vue 'inscriptions'
    # --> Cette page peut etre appelé dans siteCourse par : inscriptions:home
    path('', views.inscriptions , name='home'),

    path('supprimer/', views.supprimer_inscription, name='supprimer_inscription'),

    path('paypal', include("paypal.standard.ipn.urls")),
    path('payement_success', views.payement_success, name='payement_success'),
    path('payement_failed', views.payement_failed, name='payement_failed'),
]