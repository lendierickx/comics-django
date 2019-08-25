from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.section import Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        labels = {

        }
        widgets = {
           'name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Organization Name'
            }),
        }
