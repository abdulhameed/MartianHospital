from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class StaffSignUpForm(UserCreationForm):
    GENDER_CHOICES = [
        ('GENDER', 'Gender'),
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    first_name = forms.CharField(max_length=30, required=False, help_text='Your Given Name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Your Surname.')
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')
    phone = forms.CharField(max_length=30, required=False, help_text='Phone Number.')
    date_of_birth = forms.DateField(required=False)
    gender = forms.CharField(required=False, help_text='Gender',
                               widget=forms.Select(choices=GENDER_CHOICES))

    class Meta(UserCreationForm.Meta):
        # model = settings.AUTH_USER_MODEL
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth', 'password1', 'password2',]
        widgets = {'date_of_birth': DateInput(), }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget = DateInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class PatientSignUpForm(UserCreationForm):
    GENDER_CHOICES = [
        ('G', 'Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    first_name = forms.CharField(max_length=30, required=False, help_text='Your Given Name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Your Surname.')
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')
    phone = forms.CharField(max_length=30, required=False, help_text='Phone Number.')
    date_of_birth = forms.DateField(required=False)
    gender = forms.CharField(required=False, help_text='Gender',
                               widget=forms.Select(choices=GENDER_CHOICES))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone', 'gender', 'date_of_birth', 'password1', 'password2',)
        widgets = {'date_of_birth': DateInput(),

                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget = DateInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user
