# Generated by Django 5.1.5 on 2025-04-01 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0030_order_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='role',
        ),
    ]
