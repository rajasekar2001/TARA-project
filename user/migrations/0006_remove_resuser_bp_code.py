# Generated by Django 5.1.7 on 2025-03-20 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_resuser_bp_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resuser',
            name='bp_code',
        ),
    ]
