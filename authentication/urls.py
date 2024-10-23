# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.ObtainTokenView.as_view(), name='token_obtain'),
    path('verify/', views.verify_token, name='token_verify'),
]