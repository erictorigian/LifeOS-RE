from django.shortcuts import render
from backend.auth_utils import get_user_id_from_session

def landing(request):
    """Landing page / dashboard"""
    return render(request, "ui/landing.html")

def vision_list(request):
    user_id = get_user_id_from_session(request)
    context = {
        'user_id': user_id,
    }
    return render(request, "ui/vision_list.html", context)

def blocks_list(request):
    user_id = get_user_id_from_session(request)
    context = {
        'user_id': user_id,
    }
    return render(request, "ui/blocks_list.html", context)