# Generated by Django 5.1.5 on 2025-04-08 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superadmin',
            name='user_state',
        ),
    ]
