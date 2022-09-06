from django.contrib import admin

# Register your models here.
from staffs.models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'aptTime', 'pending_approval', 'approved')


admin.site.register(Appointment, AppointmentAdmin)
