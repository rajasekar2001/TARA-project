# Generated by Django 5.1.5 on 2025-04-02 19:07

import BusinessPartner.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0008_businesspartner_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartner',
            name='email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='businesspartner',
            name='mobile',
            field=models.CharField(max_length=15, validators=[BusinessPartner.models.validate_mobile_no], verbose_name='Mobile No'),
        ),
    ]
