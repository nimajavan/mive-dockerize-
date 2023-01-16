from django.contrib import admin
from .models import User, Profile, UserAddress
from django.contrib.auth.admin import UserAdmin as UserAdminGroup


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'is_active', 'is_admin']
    inlines = [ProfileInline]

    def has_view_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='user_permission').exists()

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='user_permission').exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='user_permission').exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        return request.user.groups.filter(name='user_permission').exists()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'last_name']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserAddress)
