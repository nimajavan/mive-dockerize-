# Generated by Django 4.1.4 on 2023-01-05 10:36

from django.conf import settings
from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0011_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='وضعیت وجود محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='product.category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='like',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='تعداد لایک ها'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='special_offer',
            field=models.BooleanField(default=False, verbose_name='پیشنهاد شگفت انگیز'),
        ),
        migrations.AlterField(
            model_name='product',
            name='views',
            field=models.BigIntegerField(default=0, verbose_name='تعداد بازید ها'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='country',
            field=models.CharField(max_length=255, verbose_name='کشور تولید کننده'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='energy',
            field=models.PositiveIntegerField(verbose_name='میزان انرژی'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='english_name',
            field=models.CharField(max_length=255, verbose_name='اسم انگلیسی محصول'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='fat',
            field=models.IntegerField(verbose_name='چربی'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='how_to_use',
            field=models.TextField(verbose_name='نحوه مصرف'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='protein',
            field=models.IntegerField(verbose_name='پرویئین'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='taste',
            field=models.CharField(max_length=255, verbose_name='مزه'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='متن توضیحات محصول'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='weight',
            field=models.PositiveIntegerField(verbose_name='وزن'),
        ),
    ]
