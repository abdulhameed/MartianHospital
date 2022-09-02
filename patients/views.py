from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin

from accounts.models import DocProfile
from patients.filters import MedicalRecordFilter
from patients.forms import BookingForm
from patients.models import MedicalRecord
from staffs.models import Appointment
from django.contrib.auth import get_user_model


class MedicalRecordListView(ListView):
    model = MedicalRecord
    # queryset = MedicalRecord.objects.all

    template_name = 'patients/MedicalRecord_listview.html'
    context_object_name = 'records'
    # paginate_by = 15

    # Context for Queryset of Un-rented Cars
    def get_context_data(self, **kwargs):
        context = super(MedicalRecordListView, self).get_context_data(**kwargs)
        context['filter'] = MedicalRecordFilter(self.request.GET, queryset=self.get_queryset())
        return context


class MedicalRecordCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalRecord
    fields = ['blood_type', 'state', 'gluten_allergy', 'peanut_allergy', 'covid_history', 'ebola_history']
    template_name = 'patients/MedicalRecord_Createview.html'

    def get_success_url(self):
        return reverse('patients:record')

    def form_valid(self, form, *args, **kwargs):
        # form.instance.medicalRecord_id = self.kwargs['pk']
        form.instance.patient = self.request.user
        form.save()
        messages.success(self.request, f'You have successfully saved your Medical Record.')
        return super().form_valid(form)

    # Ensuring that request.user is an active Patient
    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active


class DocListView(ListView):
    model = DocProfile
    # queryset = User.objects.filter(is_staff=True)
    template_name = 'patients/staffList.html'
    context_object_name = 'staffs'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(StaffListView, self).get_context_data(**kwargs)
    #     context['filter'] = StaffFilter(self.request.GET, queryset=self.get_queryset())
    #     return context


class DocDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = DocProfile
    template_name = 'patients/DoctorDetailedView.html'
    form_class = BookingForm

    def get_success_url(self):
        return reverse('patients:doc-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super(DocDetailView, self).get_context_data(*args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        print('>>>0<<<')
        form.instance.DocProfile_id = self.kwargs['pk']

        print('>>> 1<<<')

        form.instance.dateTime = self.object.dateTime

        print('>>>2<<<')

        form.instance.patient = self.request.user
        form.save()
        messages.success(self.request, f'Appointment Booking successful! the Doctor will be notified immediately.')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active


class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    fields = ['blood_type', 'state', 'gluten_allergy', 'peanut_allergy', 'covid_history', 'ebola_history']
    template_name = 'patients/Appointment_Createview.html'

    # Ensuring that request.user is an active Patient
    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active


class StatisticalChartView(TemplateView):
    template_name = 'patients/homechart.html'
    blood_type = ['GROUP_A', 'GROUP_B', 'GROUP_AB', 'GROUP_O']

    grp = MedicalRecord.objects.filter(blood_type=blood_type)
    grp_count = grp.count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grp = MedicalRecord.objects.filter(blood_type=blood_type)

        context["grp_count"] = grp.count()
        return context