from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("blocks.urls")),
    path("api/", include("visions.urls")),
    path("crm/", include("crm.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("ui.urls")),
]

# Serve static files in development
# Django's staticfiles app automatically serves files when DEBUG=True
# This is handled by django.contrib.staticfiles in INSTALLED_APPS