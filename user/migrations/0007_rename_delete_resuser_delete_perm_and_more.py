# Generated by Django 5.1.4 on 2025-02-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_resuser_email_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resuser',
            old_name='delete',
            new_name='delete_perm',
        ),
        migrations.RenameField(
            model_name='resuser',
            old_name='restore',
            new_name='restore_perm',
        ),
        migrations.AddField(
            model_name='resuser',
            name='delete_flag',
            field=models.BooleanField(default=False, verbose_name='Soft Deleted'),
        ),
    ]
