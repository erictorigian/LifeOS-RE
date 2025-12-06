"""
Custom context processors for templates.
"""
from backend.auth_utils import get_user_id_from_session


def user_context(request):
    """Add user_id to all template contexts"""
    user_id = get_user_id_from_session(request)
    return {
        'user_id': user_id,
    }

