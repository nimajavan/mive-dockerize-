# Generated by Django 4.1.4 on 2023-01-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_productcomment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='status',
            field=models.CharField(choices=[('to do', 'To Do'), ('done', 'Done'), ('failed', 'Failed')], default='to do', max_length=20, verbose_name='وضعیت'),
        ),
    ]
