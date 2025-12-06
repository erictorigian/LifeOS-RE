"""
Custom authentication backend to handle existing passwords in accounts_user table.
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import connection


class AccountsUserBackend(ModelBackend):
    """
    Custom authentication backend that can handle:
    1. Django password hashes (pbkdf2_sha256)
    2. Plain text passwords (for migration)
    3. Other password formats if needed
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        if username is None or password is None:
            return None
        
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user
            UserModel().set_password(password)
            return None
        
        # Check if password is valid
        if user.check_password(password):
            return user
        
        # If Django password check fails, try plain text comparison
        # (for existing accounts that might have plain text passwords)
        # This is a temporary migration helper - remove in production!
        if user.password == password:
            # Upgrade to hashed password
            user.set_password(password)
            user.save(update_fields=['password'])
            return user
        
        return None

