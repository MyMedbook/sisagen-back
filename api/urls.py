# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.get_user_profile, name='user-profile'),
    path('resource/', views.create_resource, name='create-resource'),
]