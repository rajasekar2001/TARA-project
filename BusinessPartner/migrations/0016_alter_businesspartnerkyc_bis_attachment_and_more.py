# Generated by Django 5.1.5 on 2025-04-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0015_alter_businesspartner_business_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartnerkyc',
            name='bis_attachment',
            field=models.ImageField(blank=True, null=True, upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='businesspartnerkyc',
            name='bis_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
