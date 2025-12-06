from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'is_master_coach']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'bio', 'location', 'website', 'birth_date')}),
        ('Profile', {'fields': ('points', 'level', 'streak', 'last_login_date', 'is_master_coach', 'supabase_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

