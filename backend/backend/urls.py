from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("blocks.urls")),
    path("api/", include("visions.urls")),
]