"""
Utilities for Supabase authentication integration.
Extracts user_id from Supabase JWT tokens and accounts_user table.
"""
import jwt
from django.conf import settings
from django.db import connection
from rest_framework.exceptions import AuthenticationFailed
import uuid


def get_user_id_from_request(request):
    """
    Get user_id from Django authenticated user for API requests.
    Falls back to default user_id for development if not authenticated.
    
    Returns:
        UUID: The user_id from authenticated user, or default for development
    """
    default_user_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    
    # Get from Django authenticated user
    if hasattr(request, 'user') and request.user.is_authenticated:
        return request.user.id
    
    # For development, return default
    # TODO: In production, raise AuthenticationFailed if not authenticated
    return default_user_id


def get_user_id_from_session(request):
    """
    Get user_id from Django authenticated user.
    Falls back to default for development if not authenticated.
    """
    default_user_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    
    # Get from Django authenticated user
    if request.user.is_authenticated:
        return request.user.id
    
    # For development, return default
    # TODO: In production, redirect to login if not authenticated
    return default_user_id

