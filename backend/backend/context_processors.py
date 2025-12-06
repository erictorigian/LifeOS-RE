"""
Custom context processors for templates.
"""
import uuid


def user_context(request):
    """Add user_id to all template contexts from Django user"""
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        # Fallback for development
        user_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    
    return {
        'user_id': user_id,
    }

