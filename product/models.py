from django.db import models
from account.models import User
from django_ckeditor_5.fields import CKEditor5Field
from jalali_date import datetime2jalali


class Category(models.Model):
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub', verbose_name='دسته تو در تو')
    sub_cat = models.BooleanField(
        default=False, verbose_name='آیا این یک زیر دسته است؟')
    slug = models.SlugField(
        allow_unicode=True, unique=True, null=True, blank=True)
    cat = models.CharField(max_length=255, verbose_name='دسته بندی')

    def __str__(self):
        return self.cat

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ViewIpAdress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = 'آی پی کاربر'
        verbose_name_plural = 'آی پی کاربران'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام محصول')
    image = models.ImageField(
        upload_to='product/', null=True, blank=True, verbose_name='تصویر محصول')
    available = models.BooleanField(
        default=True, verbose_name='وضعیت وجود محصول')
    category = models.ManyToManyField(
        Category, blank=True, verbose_name='دسته بندی')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    special_offer = models.BooleanField(
        default=False, verbose_name='پیشنهاد شگفت انگیز')
    like = models.ManyToManyField(
        User, blank=True, verbose_name='تعداد لایک ها')
    total_like = models.PositiveBigIntegerField(
        verbose_name='تعداد لایک ها', default=0)
    slug = models.SlugField(
        allow_unicode=True, unique=True, null=True, blank=True)
    view = models.ManyToManyField(ViewIpAdress, blank=True, related_name='view', verbose_name='بازدید ها')
    total_view = models.BigIntegerField(default=0, verbose_name='تعداد بازید ها')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    text = CKEditor5Field('متن توضیحات محصول', config_name='extends')
    english_name = models.CharField(
        max_length=255, verbose_name='اسم انگلیسی محصول')
    weight = models.PositiveIntegerField(verbose_name='وزن')
    country = models.CharField(max_length=255, verbose_name='کشور تولید کننده')
    taste = models.CharField(max_length=255, verbose_name='مزه')
    energy = models.PositiveIntegerField(verbose_name='میزان انرژی')
    protein = models.IntegerField(verbose_name='پرویئین')
    fat = models.IntegerField(verbose_name='چربی')
    how_to_use = models.TextField(verbose_name='نحوه مصرف')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'جزییات محصولات'


class ProductTags(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='tags')
    tags = models.CharField(max_length=50, verbose_name='تگ')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ محصولات'


class ProductComment(models.Model):
    class ProductCommentChoices(models.TextChoices):
        to_do = 'to do'
        done = 'done'
        failed = 'failed'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='commnet_related', verbose_name='محصول')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    body = models.TextField(verbose_name='متن پیام')
    status = models.CharField(max_length=20,
                              choices=ProductCommentChoices.choices, default=ProductCommentChoices.to_do, verbose_name='وضعیت', db_index=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد', null=True, blank=True)

    def shamsi_date_time(self):
        return datetime2jalali(self.created_at)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظر کاربران'
