# Generated by Django 5.1.5 on 2025-03-25 04:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_resuser_email_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resuser',
            name='email_id',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
