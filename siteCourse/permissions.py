#Fichier python pour les fonctions de permissions
import os

from django.contrib.auth.models import User
from private_storage.models import PrivateFile

from inscriptions.models import CertificatMedical


#Fonction de permission d'accès aux fichiers pdf
def custom_access_function(private_file):
    request = private_file.request
    if not request.user.is_authenticated:
        return False
    file_name = os.path.basename(private_file.relative_name)
    print(file_name)
    # Vérifie que l'utilisateur est le propriétaire ou un administrateur
    try:
        certificat = CertificatMedical.objects.get(certificat_med_name=file_name, user=request.user)
        return True  # L'utilisateur est autorisé à accéder au fichier
    except CertificatMedical.DoesNotExist:
        return request.user.is_staff or request.user.is_superuser  # Aucun certificat trouvé ou l'utilisateur n'est pas le propriétaire

