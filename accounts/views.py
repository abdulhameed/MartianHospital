from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView

from accounts.filters import DocProfileFilter
from accounts.forms import StaffSignUpForm, PatientSignUpForm
from accounts.models import DocProfile


class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'


class PatientSignUpView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = PatientSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patients:record')


class StaffSignUpView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = StaffSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patients:record')


class DoctorSearchListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DocProfile
    template_name = 'accounts/DoctorSearch_listview.html'
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super(DoctorSearchListView, self).get_context_data(**kwargs)
        context['filter'] = DocProfileFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active