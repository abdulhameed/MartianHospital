import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from patients.models import MedicalRecord
from staffs.decorators import staff_required
from staffs.models import Appointment


@login_required
@staff_required(redirect_field_name='home')
def dashboard(request):
    current_user = request.user

    today = datetime.date.today()
    current_month = today.strftime('%B')
    apm = Appointment.objects.filter(doctor=current_user, pending_approval=True)
    apm1 = Appointment.objects.filter(doctor=current_user, pending_approval=True).exclude(approved=True)[0:5]
    # apm2 = apm1.filter(pending_approval=True)[0:5]

    # import datetime
    #     today = datetime.date.today()
    #     MyModel.objects.filter(mydatefield__year=today.year,
    #                             mydatefield__month=today.month)
    #   strftime('%B')

    med_rec = MedicalRecord.objects.all

    rejected = Appointment.objects.filter(approved=False, aptTime__month=today.month, doctor=current_user)
    rejected_count = rejected.count()

    accepted = Appointment.objects.filter(approved=True, aptTime__month=today.month, doctor=current_user)
    accepted_count = accepted.count()

    context = {
        'apm2': apm1,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'med_rec': med_rec,
        'current_month': current_month
    }

    return render(request, 'staffs/StaffDashboard.html', context)


@login_required
@staff_required(redirect_field_name='home')
def accept_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.approved = True
    appointment.pending_approval = False
    appointment.save()
    messages.success(request, f'You have Accepted this Appointment')
    return redirect('staffs:staff-dashboard')


@login_required
@staff_required(redirect_field_name='home')
def reject_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.approved = False
    appointment.pending_approval = False
    appointment.save()
    messages.success(request, f'You have Rejected this Appointment')
    return redirect('staffs:staff-dashboard')
