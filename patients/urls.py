from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'patients'

urlpatterns = [
    path('', views.MedicalRecordListView.as_view(), name="record"),
    path('doctor-search/', views.DocListView.as_view(), name="doctor-search"),
    path('record-create/', views.MedicalRecordCreateView.as_view(), name="record-create"),
    path('Appointment-Create/<int:pk>/', views.AppointmentCreateView.as_view(), name="Appointment-Create"),

]
