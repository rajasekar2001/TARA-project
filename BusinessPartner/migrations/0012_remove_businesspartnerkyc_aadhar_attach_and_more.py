# Generated by Django 5.1.5 on 2025-03-05 06:32

import BusinessPartner.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0011_alter_businesspartnerkyc_bis_attachment_and_more'),
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
            name='BusinessPartnerKYCName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('aadhar_no', models.CharField(max_length=12, validators=[BusinessPartner.models.validate_aadhar_no])),
                ('aadhar_attach', models.FileField(upload_to='attachments/')),
                ('kyc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc_names', to='BusinessPartner.businesspartnerkyc')),
            ],
        ),
    ]
