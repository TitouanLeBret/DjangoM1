"""
URL configuration for siteCourse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include , re_path
from private_storage.views import PrivateStorageDetailView

from .views import accueil, parcours, login_page
from django.conf import settings
from django.conf.urls.static import static
from inscriptions.views import inscriptions
from account_own.views import account

from allauth.urls import build_provider_urlpatterns

import private_storage.urls

urlpatterns = [
#IMPORTANT ; Penser a modifier /admin en autre chose pour que les gens ne puissnet pas attérir sur la page d'admin du site
#expliquer ce choiix dans rapport :
    #si failles sur django admin, les gens ne peuvent pas trouver notre page automatiquement, donc compléxifie la chose
    path('admin_gestion/', admin.site.urls, name="admin_gestion"),
    path('', accueil , name='accueil'),
    path('accueil/', accueil , name='accueil'),
    path('inscriptions/' , include('inscriptions.urls')),
    path('parcours/' , parcours ,  name='parcours'),


    path('accounts/', include('account_own.urls') ), #quand app on ne peut pas mettre name
    path('accounts/', include('allauth.urls')),
    path('accounts/home', account , name='home'),
    #re_path utilise des regexp

    re_path(r'^private-media/', include('private_storage.urls'), name='private-media'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
