"""
URL mappings for the user API.
"""
from django.urls import path

from . import views


app_name = 'users_app'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
