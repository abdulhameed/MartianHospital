from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import accept_appointment, reject_appointment

app_name = 'staffs'

urlpatterns = [
    path('', views.dashboard, name='staff-dashboard'),
    path('accept-appointment/<int:pk>/', accept_appointment, name='accept-appointment'),
    path('reject-appointment/<int:pk>/', reject_appointment, name='reject-appointment'),
]
