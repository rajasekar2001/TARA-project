# Generated by Django 5.1.5 on 2025-03-22 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_remove_order_created_at_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01 00:00:00'),
            preserve_default=False,
        ),
    ]
