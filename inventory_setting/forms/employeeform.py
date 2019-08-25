from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.imageupload import ImageUpload
from api.models.ec.employee import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['role', ]
        labels = {

        }
        widgets = {
            'role': forms.Select(attrs={'class': u'form-control'}),
        }
