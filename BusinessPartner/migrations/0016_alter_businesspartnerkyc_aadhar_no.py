# Generated by Django 5.1.5 on 2025-03-05 07:47

import BusinessPartner.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0015_businesspartnerkyc_aadhar_attach_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartnerkyc',
            name='aadhar_no',
            field=models.CharField(default=list, max_length=12, validators=[BusinessPartner.models.validate_aadhar_no]),
        ),
    ]
