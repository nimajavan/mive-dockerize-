# Generated by Django 4.1.4 on 2023-01-05 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0004_alter_coupon_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.CharField(default=1, max_length=20, verbose_name='زمان تحویل کالا'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.IntegerField(default=1, verbose_name='کد پستی'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='تخفیف'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='وضعیت پرداخت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.IntegerField(verbose_name='تلفن همراه'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
