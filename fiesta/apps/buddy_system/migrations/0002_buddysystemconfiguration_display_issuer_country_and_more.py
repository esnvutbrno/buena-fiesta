# Generated by Django 4.0.2 on 2022-07-24 09:38

import uuid

import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sections', '0006_alter_section_space_slug'),
        ('buddy_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='display_issuer_country',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='display_issuer_faculty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='display_issuer_gender',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='display_issuer_picture',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='display_issuer_university',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='matching_policy',
            field=models.CharField(choices=[('manual-by-editor', 'Manual by editors'), ('manual-by-member', 'Manual by members'), ('same-faculty', 'Limited by faculty'), ('same-faculty-limited', 'Limited by faculty till limit')], default='manual-by-editor', help_text='Manual by editors: Matching done manualy only by editors. <br />Manual by members: Matching done manualy also by members. <br />Limited by faculty: Matching done manualy by members themselfs, but limited to the same faculty. <br />Limited by faculty till limit: Matching done manualy by members themselfs, but limited to same faculty tillthe rolling limit - limitation is not enabled after reaching the rolling limit.', max_length=32),
        ),
        migrations.AddField(
            model_name='buddysystemconfiguration',
            name='rolling_limit',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BuddyRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('state', models.CharField(choices=[('created', 'Created'), ('matched', 'Matched'), ('cancelled', 'Cancelled')], default='created', max_length=16, verbose_name='state')),
                ('matched_at', models.DateTimeField(blank=True, null=True, verbose_name='matched at')),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='buddy_system_issued_requests', to=settings.AUTH_USER_MODEL, verbose_name='issuer')),
                ('matched_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='buddy_system_matched_requests', to=settings.AUTH_USER_MODEL, verbose_name='matched by')),
                ('responsible_section', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='buddy_system_requests', to='sections.section', verbose_name='responsible section')),
            ],
            options={
                'verbose_name': 'buddy request',
                'verbose_name_plural': 'buddy requests',
            },
        ),
    ]
