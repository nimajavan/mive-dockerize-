# Generated by Django 4.1.4 on 2023-01-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productcomment_status_alter_category_cat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='product/'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='status',
            field=models.CharField(choices=[('to do', 'To Do'), ('done', 'Done')], default='to do', max_length=20, verbose_name='وضعیت'),
        ),
    ]