from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from accounts.forms import StaffSignUpForm, PatientSignUpForm


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