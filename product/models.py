from django.db import models
from account.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db import models as jmodels


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


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام محصول')
    image = models.ImageField(
        upload_to='product/', null=True, blank=True, verbose_name='تصویر محصول')
    available = models.BooleanField(
        default=True, verbose_name='وضعیت وجود محصول')
    category = models.ManyToManyField(
        Category, blank=True, verbose_name='دسته بندی')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    special_offer = models.BooleanField(
        default=False, verbose_name='پیشنهاد شگفت انگیز')
    like = models.ManyToManyField(
        User, blank=True, verbose_name='تعداد لایک ها')
    total_like = models.PositiveIntegerField(verbose_name='تعداد لایک ها')
    views = models.BigIntegerField(default=0, verbose_name='تعداد بازید ها')
    slug = models.SlugField(
        allow_unicode=True, unique=True, null=True, blank=True)

    def total_like(self):
        return self.like.count()

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
        to_do = 'to do',
        done = 'done'

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='commnet_related', verbose_name='محصول')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    body = models.TextField(verbose_name='متن پیام')
    status = models.CharField(max_length=20,
                              choices=ProductCommentChoices.choices, default=ProductCommentChoices.to_do, verbose_name='وضعیت')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظر کاربران'


class ViewIpAdress(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=50)

    def __str__(self):
        return self.ip_addr

    class Meta:
        verbose_name = 'آی پی کاربر'
        verbose_name_plural = 'آی پی کاربران'
