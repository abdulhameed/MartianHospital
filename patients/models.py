from django.db import models
from django.conf import settings


# Create your models here.
class MedicalRecord(models.Model):
    GROUP_A = 'A'
    GROUP_B = 'B'
    GROUP_AB = 'AB'
    GROUP_O = 'O'

    BLOOD_TYPE_CHOICES = [
        (GROUP_A, 'GRP_A'),
        (GROUP_B, 'GRP_B'),
        (GROUP_AB, 'GRP_AB'),
        (GROUP_O, 'GRP_O'),
    ]

    STATE_DEF = 'Abuja'
    STATE_CHOICES = [
        ('Abuja', "Abuja"),
        ('AB', "Abia"),
        ('AD', "Adamawa"),
        ('AK', "Akwa Ibom"),
        ('AN', "Anambra"),
        ('BA', "Bauchi"),
        ('BY', "Bayelsa"),
        ('BE', "Benue"),
        ('BO', "Borno"),
        ('CR', "Cross River"),
        ('DE', "Delta"),
        ('EB', "Ebonyi"),
        ('ED', "Edo"),
        ('EK', "Ekiti"),
        ('EN', "Enugu"),
        ('GO', "Gombe"),
        ('IM', "Imo"),
        ('JI', "Jigawa"),
        ('KD', "Kaduna"),
        ('KN', "Kano"),
        ('KT', "Katsina"),
        ('KE', "Kebbi"),
        ('KO', "Kogi"),
        ('Kw', "Kwara"),
        ('Lag', "Lagos"),
        ('NA', "Nassarawa"),
        ('NI', "Niger"),
        ('OG', "Ogun"),
        ('ON', "Ondo"),
        ('OS', "Osun"),
        ('OY', "Oyo"),
        ('PL', "Plateau"),
        ('RI', "Rivers"),
        ('SO', "Sokoto"),
        ('TA', "Taraba"),
        ('YO', "Yobe"),
        ('ZA', "Zamfara")
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    blood_type = models.CharField(max_length=2, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    state = models.CharField(max_length=7, default=STATE_DEF, choices=STATE_CHOICES, blank=True, null=True)
    gluten_allergy = models.BooleanField(default=False)
    peanut_allergy = models.BooleanField(default=False)
    covid_history = models.BooleanField(default=False)
    ebola_history = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient.first_name+" "+self.patient.last_name}'
