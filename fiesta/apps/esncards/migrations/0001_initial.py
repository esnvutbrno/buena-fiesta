# Generated by Django 4.0.2 on 2022-02-12 13:02

import uuid

import django.core.serializers.json
import django_countries.fields
import django_extensions.db.fields
import django_lifecycle.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ESNcardApplication",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="last name"),
                ),
                (
                    "nationality",
                    django_countries.fields.CountryField(
                        max_length=2, verbose_name="nationality"
                    ),
                ),
                ("birth_date", models.DateField(verbose_name="birth date")),
                (
                    "state",
                    models.TextField(
                        choices=[
                            ("created", "Created"),
                            ("accepted", "Accepted"),
                            ("ready", "Ready to pickup"),
                            ("issued", "Issued"),
                            ("declined", "Declined"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="created",
                        max_length=16,
                        verbose_name="state",
                    ),
                ),
                (
                    "history",
                    models.JSONField(
                        default=list,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
            ],
            options={
                "verbose_name": "ESNcard application",
                "verbose_name_plural": "ESNcard applications",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
