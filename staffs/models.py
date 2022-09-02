from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


# Appointment model

class Appointment(models.Model):
    # User = get_user_model()
    # USER1 = User.objects.get(pk='1')

    staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staff',
                              on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.SET_NULL, null=True)
    dateTime = models.DateTimeField(blank=True, null=True)
    pending_approval = models.BooleanField(default=True, null=True)
    approved = models.BooleanField(default=False, null=True)
