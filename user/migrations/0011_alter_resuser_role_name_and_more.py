# Generated by Django 5.1.5 on 2025-03-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_resuser_managers_remove_resuser_delete_perm_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resuser',
            name='role_name',
            field=models.CharField(choices=[('Project Owner', 'Project Owner'), ('Super Admin', 'Super Admin'), ('staff', 'Key User'), ('User', 'User'), ('Craftsman', 'Craftsman'), ('customer', 'One Time User')], max_length=50),
        ),
        migrations.AlterField(
            model_name='roledashboardmapping',
            name='role',
            field=models.CharField(choices=[('Project Owner', 'Project Owner'), ('Super Admin', 'Super Admin'), ('staff', 'Key User'), ('User', 'User'), ('Craftsman', 'Craftsman'), ('customer', 'One Time User')], max_length=50),
        ),
    ]
