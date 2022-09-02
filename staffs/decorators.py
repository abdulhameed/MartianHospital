from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


class DriverOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_patient


class OwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active


def is_patient(user):
    return user.is_active and user.is_patient


def patient_required(function=is_patient, redirect_field_name='patients:record', login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a Patient,
    redirects to the log-in page if necessary.
    '''
    return user_passes_test(
        function, login_url, redirect_field_name
    )


def is_staff(user):
    return user.is_active and user.is_staff


def staff_required(function=is_staff, redirect_field_name='staffs:staff-dashboard', login_url='login'):
    """
    Decorator for views that checks that the logged in user is a Staff,
    redirects to the log-in page if necessary.
    """
    return user_passes_test(
        function, login_url, redirect_field_name
    )
