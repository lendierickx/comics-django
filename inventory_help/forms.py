from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.helprequest import HelpRequest


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['subject', 'subject_url', 'message']
        labels = {

        }
        widgets = {
            'subject': forms.Select(attrs={'class': u'form-control'}),
            'subject_url': forms.TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter URL of Issue'
            }),
            'message': forms.Textarea(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Message',
                'style':'height:200px;',
            }),
        }
