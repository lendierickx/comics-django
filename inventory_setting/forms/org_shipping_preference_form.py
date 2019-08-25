from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.section import Section
from api.models.ec.orgshippingpreference import OrgShippingPreference


class OrgShippingPreferenceForm(forms.ModelForm):
    class Meta:
        model = OrgShippingPreference
        fields = ['is_pickup_only',]
        labels = {

        }
#        widgets = {
#           'name': TextInput(attrs={
#                'class': u'form-control mb-lg',
#                'placeholder': u'Enter Organization Name'
#            }),
#        }
