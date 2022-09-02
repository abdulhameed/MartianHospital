from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', views.SignUpView.as_view(), name="register"),
    path('register/staff/', views.StaffSignUpView.as_view(), name="staff-register"),
    path('register/patient/', views.PatientSignUpView.as_view(), name="patient-register"),
    # path('staff-profile/', views.staff_profile_view, name="staff-profile"),
    # path('patient-profile/', views.patient_profile_view, name="patient-profile"),
    # path('patient/profile/<int:pk>/', views.DriverProfilePageView.as_view(), name='driver-profile-view'),
]
