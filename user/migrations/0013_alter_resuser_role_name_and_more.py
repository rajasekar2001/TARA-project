# Generated by Django 5.1.5 on 2025-03-24 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_resuser_role_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resuser',
            name='role_name',
            field=models.CharField(choices=[('Project Owner', 'Project Owner'), ('Super Admin', 'Super Admin'), ('Key User', 'Key User'), ('User', 'User'), ('Craftsman', 'Craftsman'), ('Walking Customer', 'Walking Customer')], max_length=50),
        ),
        migrations.AlterField(
            model_name='roledashboardmapping',
            name='role',
            field=models.CharField(choices=[('Project Owner', 'Project Owner'), ('Super Admin', 'Super Admin'), ('Key User', 'Key User'), ('User', 'User'), ('Craftsman', 'Craftsman'), ('Walking Customer', 'Walking Customer')], max_length=50),
        ),
    ]
