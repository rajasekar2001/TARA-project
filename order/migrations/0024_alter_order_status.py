# Generated by Django 5.1.5 on 2025-03-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_order_created_at_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
