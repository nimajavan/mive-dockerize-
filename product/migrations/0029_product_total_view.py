# Generated by Django 4.1.4 on 2023-01-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_alter_product_view_alter_viewipadress_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_view',
            field=models.BigIntegerField(default=0),
        ),
    ]
