from django.urls import path
from . import views

urlpatterns = [
    # other urls
    path('accounts/register/', views.register, name='register'),
]
