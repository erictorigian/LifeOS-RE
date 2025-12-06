from django.urls import path
from .views import vision_list
from .auth_views import login_view, auth_callback, logout_view, set_user_id

app_name = 'ui'

urlpatterns = [
    path("visions/", vision_list, name="vision-list"),
    path("login/", login_view, name="login"),
    path("auth/callback/", auth_callback, name="auth_callback"),
    path("logout/", logout_view, name="logout"),
    path("set-user-id/", set_user_id, name="set_user_id"),  # Development only
]