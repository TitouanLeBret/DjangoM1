# Generated by Django 5.1.3 on 2024-12-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscriptions', '0002_remove_inscriptioncourse_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscriptioncourse',
            name='lien_vers_certificat',
        ),
        migrations.AddField(
            model_name='inscriptioncourse',
            name='certificat_med',
            field=models.FileField(null=True, upload_to='siteCourse/media'),
        ),
    ]
