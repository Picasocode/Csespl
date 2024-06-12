# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    ordering = ['name','role']
    list_display = ['name', 'email', 'register_no', 'role', 'department', 'is_staff','profile_picture_tag']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'role', 'department']
    search_fields = ['email', 'name', 'register_no', 'role', 'department']

    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'register_no', 'profile_picture', 'batch', 'role', 'department')}),
        (_('Permissions'), {'fields': ('is_active','is_staff')}),  # Only include is_active for non-superusers
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'register_no', 'profile_picture', 'batch', 'role', 'department'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(pk=request.user.pk)
        return qs

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            return (
                (None, {'fields': ('email', 'password')}),
                (_('Personal info'), {'fields': ('name', 'register_no', 'profile_picture', 'batch', 'role', 'department')}),
            )

    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />'.format(obj.profile_picture.url))
        return "-"
    profile_picture_tag.short_description = 'Profile Picture'

admin.site.register(CustomUser, UserAdmin)
