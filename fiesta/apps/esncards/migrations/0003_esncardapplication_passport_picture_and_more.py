# Generated by Django 4.0.2 on 2022-02-22 13:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esncards', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL('TRUNCATE esncards_esncardapplication;'),
        migrations.AddField(
            model_name='esncardapplication',
            name='passport_picture',
            field=models.ImageField(default=None, storage=apps.files.storage.NamespacedFilesStorage('esncard-application-picture'), upload_to=apps.files.storage.NamespacedFilesStorage.upload_to, verbose_name='passport-sized face picture'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='esncardapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='esncard_applications', to=settings.AUTH_USER_MODEL, verbose_name='issuer'),
        ),
    ]