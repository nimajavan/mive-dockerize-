from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('please enter username')

        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.BigIntegerField(
        unique=True, verbose_name='شماره همراه')
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادیمن')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'کاربران'
        verbose_name_plural = 'کاربران'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='profile')
    name = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name='نام')
    last_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='نام خانوادگی')
    profile_image = models.ImageField(
        upload_to='profile/', null=True, blank=True, verbose_name='تصویر پروفایل')

    def __str__(self):
        return str(self.user.phone)

    class Meta:
        verbose_name = 'پروفایل کاربران'
        verbose_name_plural = 'پروفایل کاربران'

    # def save(self, *args, **kwargs):
    #     super().save()

    #     if self.profile_iamge.path:
    #         img = Image.open(self.profile_image.path)
    #         print(img)

    #         if img.height > 500 or img.width > 500:
    #             new_img = (500, 500)
    #             img.thumbnail(new_img)
    #             img.save(self.profile_image.path)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    post_code = models.IntegerField()

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = 'آدرس کاربران'
        verbose_name_plural = 'آدرس کاربران'