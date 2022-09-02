import django_filters
from django.conf import settings

from accounts.models import DocProfile
from .models import MedicalRecord


class MedicalRecordFilter(django_filters.FilterSet):

    class Meta:
        model = MedicalRecord
        fields = {'state': ['exact'], 'blood_type': ['exact']}


# class StaffFilter(django_filters.FilterSet):
#
#     class Meta:
#         model = StaffProfile
        # fields = {'first_name': ['exact'], 'last_name': ['exact'], 'state': ['exact']}
