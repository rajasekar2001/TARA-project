# Generated by Django 5.1.5 on 2025-03-06 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0016_alter_businesspartnerkyc_aadhar_no'),
        ('order', '0008_remove_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bp_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BusinessPartner.businesspartner'),
        ),
    ]
