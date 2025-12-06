from django.shortcuts import render
from backend.auth_utils import get_user_id_from_session

def vision_list(request):
    user_id = get_user_id_from_session(request)
    context = {
        'user_id': user_id,
    }
    return render(request, "ui/vision_list.html", context)