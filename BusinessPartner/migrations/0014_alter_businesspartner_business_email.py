# Generated by Django 5.1.5 on 2025-04-03 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0013_alter_businesspartner_business_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartner',
            name='business_email',
            field=models.EmailField(max_length=255),
        ),
    ]
