from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Contacts
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<uuid:pk>/update/', views.contact_update, name='contact_update'),
    path('contacts/<uuid:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # Deals
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/create/', views.deal_create, name='deal_create'),
    path('deals/<uuid:pk>/update/', views.deal_update, name='deal_update'),
    path('deals/<uuid:pk>/delete/', views.deal_delete, name='deal_delete'),
    path('deals/<uuid:pk>/detail/', views.deal_detail_json, name='deal_detail_json'),
    
    # Interactions
    path('interactions/', views.interaction_list, name='interaction_list'),
    path('interactions/create/', views.interaction_create, name='interaction_create'),
    path('interactions/<uuid:pk>/update/', views.interaction_update, name='interaction_update'),
    path('interactions/<uuid:pk>/delete/', views.interaction_delete, name='interaction_delete'),
]

