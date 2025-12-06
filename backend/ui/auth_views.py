"""
Supabase authentication views for Django templates.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import uuid
import jwt
from backend.auth_utils import get_user_id_from_session


def login_view(request):
    """Display login page with Supabase auth options"""
    # If already logged in, redirect to dashboard
    user_id = get_user_id_from_session(request)
    if user_id and user_id != uuid.UUID('11111111-1111-1111-1111-111111111111'):
        return redirect('crm:dashboard')
    
    # Get Supabase URL from settings or use default
    supabase_url = getattr(settings, 'SUPABASE_URL', 'https://wkxedsjdkkczreprjsvc.supabase.co')
    
    context = {
        'supabase_url': supabase_url,
    }
    return render(request, 'ui/login.html', context)


def auth_callback(request):
    """
    Handle Supabase authentication callback.
    Extracts user_id from the token and stores it in session.
    """
    # Get token from query params or fragment (Supabase redirects with hash)
    token = request.GET.get('access_token') or request.GET.get('token')
    
    if not token:
        # Try to get from POST data
        token = request.POST.get('access_token')
    
    if token:
        try:
            # Decode JWT to get user_id
            decoded = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded.get('sub')
            
            if user_id:
                # Store user_id in session
                request.session['user_id'] = str(user_id)
                request.session['access_token'] = token
                messages.success(request, 'Successfully logged in!')
                return redirect('crm:dashboard')
        except (jwt.DecodeError, ValueError, KeyError) as e:
            messages.error(request, f'Invalid authentication token: {str(e)}')
    
    messages.error(request, 'Authentication failed. Please try again.')
    return redirect('ui:login')


def logout_view(request):
    """Logout user by clearing session"""
    request.session.flush()
    messages.success(request, 'Successfully logged out!')
    return redirect('ui:login')


def set_user_id(request):
    """
    Development helper: Manually set user_id in session.
    Remove this in production!
    """
    if not settings.DEBUG:
        messages.error(request, 'This endpoint is only available in development mode.')
        return redirect('crm:dashboard')
    
    user_id = request.GET.get('user_id')
    if user_id:
        try:
            uuid.UUID(user_id)  # Validate it's a valid UUID
            request.session['user_id'] = user_id
            messages.success(request, f'User ID set to {user_id}')
        except ValueError:
            messages.error(request, 'Invalid user_id format. Must be a UUID.')
    
    return redirect('crm:dashboard')

