"""
Django User model that syncs with Supabase accounts_user table.
Matches the existing table structure exactly.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Manager for custom User model"""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and save a regular user"""
        if not username:
            raise ValueError('The Username field must be set')
        if email:
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that maps to Supabase accounts_user table.
    Matches the existing table structure exactly.
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128)  # Django will handle this via AbstractBaseUser
    
    # Django auth fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Additional fields from accounts_user table
    points = models.IntegerField(default=0, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    streak = models.IntegerField(default=0, blank=True, null=True)
    last_login_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_master_coach = models.BooleanField(default=False)
    supabase_id = models.CharField(max_length=255, blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] if email else []
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        managed = True  # Django manages this table
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the short name of the user"""
        return self.first_name or self.username

