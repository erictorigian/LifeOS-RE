from django.urls import path
from .views import vision_list, blocks_list

app_name = 'ui'

urlpatterns = [
    path("visions/", vision_list, name="vision_list"),
    path("blocks/", blocks_list, name="blocks_list"),
]