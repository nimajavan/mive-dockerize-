from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    create = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    phone = models.IntegerField(verbose_name='تلفن همراه')
    address = models.TextField(verbose_name='آدرس')
    postal_code = models.IntegerField(verbose_name='کد پستی')
    delivery_date = models.CharField(
        max_length=20, verbose_name='زمان تحویل کالا')
    sent = models.BooleanField(default=False, verbose_name='ارسال شده؟')

    def __str__(self):
        return str(self.user.phone)

    def total_price(self):
        price = sum(item.price() for item in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * price
            return int(price - discount_price)
        return price

    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارشات'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_item', verbose_name='سفارش مربوطه')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.user.phone)

    def price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'آیتم های سفارشات'
        verbose_name_plural = 'آیتم های سفارشات'


class Coupon(models.Model):
    code = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.IntegerField()

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف'


class PaymentChoices(models.TextChoices):
    success = 'success'
    faild = 'faild'


class PaymentHistory(models.Model):
    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.TextField(default='-')
    card_number = models.TextField(default="****")
    idpay_track_id = models.IntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)

    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + "  |  " + self.order_id + "  |  " + str(self.status)

    class Meta:
        verbose_name = 'تاریخچه پرداخت ها'
        verbose_name_plural = 'تاریخچه پرداخت ها'
