from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.agent_login, name='login'),
    path('logout/', views.agent_logout, name='logout'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/<int:pk>/', views.agent_detail, name='agent_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/properties/new/', views.property_create, name='property_create'),
    path('dashboard/properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('dashboard/properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
]
