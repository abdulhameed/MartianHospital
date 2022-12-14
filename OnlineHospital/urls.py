"""OnlineHospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

import patients
from patients.views import MedicalRecordListView

urlpatterns = [
    path('', patients.views.patientsView, name='home'),
    path('1/', patients.views.patientsView, name='home1'),
    path('admin/', admin.site.urls),
    path('patient/', include('patients.urls')),
    path('patients-list/', MedicalRecordListView.as_view(), name='patients-list'),
    path('staff/', include('staffs.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('booking-confirmed/', TemplateView.as_view(template_name="patients/booking_confirmed.html"),
         name='booking-confirmed'),

]
