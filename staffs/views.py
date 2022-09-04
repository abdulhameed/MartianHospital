from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from patients.models import MedicalRecord
from staffs.decorators import staff_required
from staffs.models import Appointment


@login_required
@staff_required(redirect_field_name='owner:owner-dashboard')
def dashboard(request):
    current_user = request.user

    apm = Appointment.objects.filter(doctor=current_user)[0:5]
    apm1 = Appointment.objects.filter(doctor=current_user).exclude(approved=True)
    apm2 = apm1.filter(pending_approval=True)[0:5]

    med_rec = MedicalRecord.objects.all

    rejected = Appointment.objects.filter(approved=False)
    rejected_count = rejected.count()

    accepted = Appointment.objects.filter(approved=True)
    accepted_count = accepted.count()

    context = {
        'apm2': apm2,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'med_rec': med_rec,
    }

    return render(request, 'staffs/StaffDashboard.html', context)


@login_required
@staff_required(redirect_field_name='owner:owner-dashboard')
def accept_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.approved = True
    appointment.pending_approval = False
    appointment.save()
    messages.success(request, f'You have Accepted this Appointment')
    return redirect('staffs:staff-dashboard')


@login_required
@staff_required(redirect_field_name='owner:owner-dashboard')
def reject_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.approved = False
    appointment.pending_approval = False
    appointment.save()
    messages.success(request, f'You have Rejected this Appointment')
    return redirect('staffs:staff-dashboard')
