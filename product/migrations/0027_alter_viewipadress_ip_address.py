# Generated by Django 4.1.4 on 2023-01-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_alter_product_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewipadress',
            name='ip_address',
            field=models.CharField(max_length=255, verbose_name='آدرس آی پی'),
        ),
    ]