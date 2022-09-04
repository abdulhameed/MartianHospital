from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
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

    template_name = 'patients/MedicalRecord_listview.html'
    context_object_name = 'records'

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


class DocListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DocProfile
    # queryset = User.objects.filter(is_staff=True)
    template_name = 'patients/staffList.html'
    # context_object_name = 'staffs'

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()

    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active


class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    fields = ['aptTime']
    template_name = 'patients/Appointment-Createview.html'

    def form_valid(self, form, *args, **kwargs):
        form.instance.doctor_id = self.kwargs['pk'] #TODO change to doctor instance
        form.instance.patient = self.request.user
        ###############################################
        User = get_user_model()
        sender_email = 'instaridenigeria@gmail.com'
        doctor_email = User.objects.get(id=self.kwargs['pk'])
        doctor_email = doctor_email.email
        template = render_to_string('patients/booking_email_template.html', {'doctor':User.objects.get(id=self.kwargs['pk']),'patient':self.request.user.first_name, 'aptTime':form.cleaned_data.get('aptTime')})

            # Send Email Logic
        msg = EmailMessage(
            'Appointment booking from ' + self.request.user.first_name,  # Subject
            template,  # Message
            sender_email,  # From
            [doctor_email, 'giwabdul@gmail.com'],  # To
            headers={'Message-ID': 'foo'},
        )
        msg.send(fail_silently=False)
        messages.success(self.request, f'Appointment Booking successful! the Doctor will be notified immediately.')

        return super(AppointmentCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('patients:doctor-search')


    # Ensuring that request.user is an active Patient
    def test_func(self):
        return self.request.user.is_patient and self.request.user.is_active


class StatisticalChartView(TemplateView):
    template_name = 'patients/homechart.html'
    blood_type = ['GROUP_A', 'GROUP_B', 'GROUP_AB', 'GROUP_O']

    medical_records = MedicalRecord.objects.all()

    # grp = MedicalRecord.objects.filter(blood_type=blood_type)
    # grp_count = grp.count()

    # context['count'] = context['tasks'].count()
    # context['your_qset'] = YourModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gluten_allergy'] = MedicalRecord.objects.filter(gluten_allergy = True).count
        context['peanut_allergy'] = MedicalRecord.objects.filter(peanut_allergy = True).count
        context['covid_history'] = MedicalRecord.objects.filter(covid_history=True).count
        context['ebola_history'] = MedicalRecord.objects.filter(ebola_history=True).count

        return context


############################################################################################################
def patientsView(request):
    gluten_allergy = MedicalRecord.objects.filter(gluten_allergy = True).count()
    gluten_allergy = int(gluten_allergy)
    print('Number of Gluten Allergy patients Are',gluten_allergy)

    peanut_allergy = MedicalRecord.objects.filter(peanut_allergy = True).count()
    peanut_allergy = int(peanut_allergy)
    print('Number of Peanut Allergy patients Are',peanut_allergy)

    covid_history = MedicalRecord.objects.filter(covid_history=True).count()
    covid_history = int(covid_history)
    print('Number of Covid History patients Are',covid_history)

    ebola_history = MedicalRecord.objects.filter(ebola_history=True).count()
    ebola_history = int(ebola_history)
    print('Number of Ebola History patients Are',ebola_history)

    GROUP_A = MedicalRecord.objects.filter(blood_type='A').count()
    # GERT = MedicalRecord.objects.filter(blood_type='A')
    # GROUP_A = int(GROUP_A)
    print('Number of Male Are',GROUP_A)

    GROUP_B = MedicalRecord.objects.filter(blood_type='B').count()
    # GROUP_B = int(GROUP_B)
    print('Number of patients with Group B Are ' ,GROUP_B)

    GROUP_AB = MedicalRecord.objects.filter(blood_type='AB').count()
    # GROUP_AB = int(GROUP_AB)
    print('Number of patients with Group AB Are', GROUP_AB)

    GROUP_O = MedicalRecord.objects.filter(blood_type='O').count()
    # GROUP_O = int(GROUP_O)
    print('Number of patients with Group O Are', GROUP_O)

    blood_type = ['GROUP_A', 'GROUP_B', 'GROUP_AB', 'GROUP_O']
    blood_type_count = [GROUP_A, GROUP_B, GROUP_AB, GROUP_O]

    condition_list = ['Gluten Allergy', 'Peanut Allergy', 'Covid History', 'Ebola History']
    condition_list_count = [gluten_allergy, peanut_allergy, covid_history, ebola_history]
    context = {'condition_list':condition_list,
               'condition_list_count':condition_list_count,
               'blood_type':blood_type,
               'blood_type_count':blood_type_count}
    return render(request, 'patients/homechart1F.html', context)