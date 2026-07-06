from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
]
