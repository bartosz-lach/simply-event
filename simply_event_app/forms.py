from datetime import timedelta

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from tempus_dominus.widgets import DatePicker, DateTimePicker

from simply_event_app.models import Event, Guest

custom_text_input = forms.TextInput(
    attrs={
        'class': 'form-control'
    }
)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': custom_text_input,
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'delay']
        widgets = {
            'name': custom_text_input,
            'delay': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

    # def clean_delay(self):
    #     input = self.cleaned_data['delay']
    #     delay = timedelta(minutes=input)
    #     return delay


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('owner', 'create_date')
        widgets = {
            'name': custom_text_input,
            'location': custom_text_input,
            'start_date': forms.DateTimeInput(

                format='%m/%d/%Y %H:%M',
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#start_date_picker',
                    'placeholder': 'Start Date'

                }
            ),
            'end_date': forms.DateTimeInput(
                format='%m/%d/%Y %H:%M',

                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#end_date_picker',
                    'placeholder': 'End Date'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'is_public': forms.CheckboxInput(
            #     attrs={
            #         'class': 'form-check-input'
            #     })
        }

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        # if end_date is None:
        #     return end_date

        if end_date is not None and end_date < start_date:
            raise ValidationError('End date cannot be earlier than start date')

        return end_date

# class EventForm(forms.Form):
#     start_date = forms.DateField(widget=DatePicker())
