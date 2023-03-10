# Generated by Django 4.1.4 on 2023-01-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_productcomment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewIpAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آی پی')),
            ],
            options={
                'verbose_name': 'آی پی کاربر',
                'verbose_name_plural': 'آی پی کاربران',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveBigIntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_like',
            field=models.PositiveBigIntegerField(default=0, verbose_name='تعداد لایک ها'),
        ),
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, null=True, to='product.viewipadress'),
        ),
    ]
