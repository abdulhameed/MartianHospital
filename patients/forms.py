from django import forms
from staffs.models import Appointment


class DateTimeInput(forms.DateTimeInput):
    input_type = 'dateTime'


class BookingForm(forms.ModelForm):
    dateTime = forms.DateTimeField(widget=DateTimeInput, required=True)
    class Meta:
        model = Appointment
        fields = ['dateTime']
        widgets = {'dateTime': DateTimeInput(), }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dateTime"].widget = DateTimeInput()
