from django.contrib import admin
from .models import User, Profile, UserAddress
from django.contrib.auth.admin import UserAdmin as UserAdminGroup


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'is_active', 'is_admin']
    inlines = [ProfileInline]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'last_name']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserAddress)
