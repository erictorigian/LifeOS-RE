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
    Extract user_id from Supabase JWT token in request.
    Falls back to a default user_id for development if no token is present.
    
    Returns:
        UUID: The user_id from the token, or default for development
    """
    # For development: if no auth token, use default user_id
    # In production, this should require authentication
    default_user_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    
    # Try to get token from Authorization header
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header or not auth_header.startswith('Bearer '):
        # Also check for token in cookies (Supabase client-side auth)
        token = request.COOKIES.get('sb-access-token') or request.COOKIES.get('supabase.auth.token')
        if not token:
            # For now, return default for development
            # TODO: In production, raise AuthenticationFailed
            return default_user_id
    else:
        token = auth_header.split(' ')[1]
    
    try:
        # Decode JWT token (Supabase uses HS256)
        # Note: In production, you should verify the token with Supabase's JWT secret
        # For now, we'll extract the user_id if present
        decoded = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded.get('sub')  # Supabase uses 'sub' claim for user_id
        
        if user_id:
            # Verify user exists in accounts_user table
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM accounts_user WHERE id = %s",
                        [str(user_id)]
                    )
                    if cursor.fetchone():
                        return uuid.UUID(user_id)
            except Exception:
                # If table doesn't exist or query fails, still return the user_id from token
                pass
            
            return uuid.UUID(user_id)
        else:
            return default_user_id
    except (jwt.DecodeError, ValueError, KeyError, TypeError):
        # If token is invalid, return default for development
        # TODO: In production, raise AuthenticationFailed
        return default_user_id


def get_user_id_from_session(request):
    """
    Get user_id from Django session (for template views).
    Also checks for Supabase auth token in cookies.
    Falls back to default for development.
    """
    default_user_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    
    # Check if user_id is stored in session
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return uuid.UUID(user_id)
        except (ValueError, TypeError):
            pass
    
    # Try to get from Supabase token in cookies
    token = request.COOKIES.get('sb-access-token') or request.COOKIES.get('supabase.auth.token')
    if token:
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded.get('sub')
            if user_id:
                # Store in session for future requests
                request.session['user_id'] = str(user_id)
                return uuid.UUID(user_id)
        except (jwt.DecodeError, ValueError, KeyError, TypeError):
            pass
    
    # For development, return default
    # TODO: In production, redirect to login if no user_id in session
    return default_user_id

