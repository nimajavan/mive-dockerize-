# Generated by Django 4.1.4 on 2023-01-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_viewipadress_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, to='product.viewipadress'),
        ),
    ]
