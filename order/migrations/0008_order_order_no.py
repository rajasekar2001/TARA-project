# Generated by Django 5.1.5 on 2025-03-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_packorder_order_remove_packorder_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_no',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
