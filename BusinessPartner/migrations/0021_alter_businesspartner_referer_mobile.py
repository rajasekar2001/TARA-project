# Generated by Django 5.1.5 on 2025-03-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0020_alter_businesspartner_referer_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspartner',
            name='referer_mobile',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
