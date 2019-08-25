from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'first_name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter First Name'
            }),
            'last_name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Last Name'
            }),
            'email': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Email Address'
            }),
        }

    old_password = forms.CharField(
        label='Old Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Enter Old Password'
        }),
        required=False,
    )

    password = forms.CharField(
        label='New Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Enter New Password'
        }),
        required=False,
    )

    password_repeated = forms.CharField(
        label='Repeat Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Enter Password Again'
        }),
        required=False,
    )

    def clean_password_repeated(self):
        password = self.cleaned_data['password']
        password_repeated = self.cleaned_data['password_repeated']
        if password != password_repeated:
            raise forms.ValidationError("Passwords do not match.")
        return password_repeated
