from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.property_list, name='list'),
    path('listings/<slug:slug>/', views.property_detail, name='detail'),
]
