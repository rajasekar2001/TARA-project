# Generated by Django 5.1.5 on 2025-03-05 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0013_businesspartnerkyc_aadhar_attach_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businesspartnerkyc',
            name='aadhar_attach',
        ),
        migrations.RemoveField(
            model_name='businesspartnerkyc',
            name='aadhar_no',
        ),
        migrations.RemoveField(
            model_name='businesspartnerkyc',
            name='name',
        ),
        migrations.CreateModel(
            name='AadharDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('aadhar_no', models.CharField(max_length=12)),
                ('aadhar_attach', models.URLField()),
                ('business_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aadhar_details', to='BusinessPartner.businesspartnerkyc')),
            ],
        ),
    ]
