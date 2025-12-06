from django.urls import path
from .views import vision_list

app_name = 'ui'

urlpatterns = [
    path("visions/", vision_list, name="vision-list"),
]