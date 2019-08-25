from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.orgshippingrate import OrgShippingRate


class OrgShippingRateForm(forms.ModelForm):
    class Meta:
        model = OrgShippingRate
        fields = ['country','comics_rate1','comics_rate2','comics_rate3','comics_rate4','comics_rate5','comics_rate6','comics_rate7','comics_rate8','comics_rate9','comics_rate10',]
        labels = {
            'comics_rate1':'1-10 Comics Rate:',
            'comics_rate2':'11-20 Comics Rate:',
            'comics_rate3':'21-30 Comics Rate:',
            'comics_rate4':'31-40 Comics Rate:',
            'comics_rate5':'41-50 Comics Rate:',
            'comics_rate6':'51-74  Comics Rate:',
            'comics_rate7':'75-100 Comics Rate:',
            'comics_rate8':'101-150 Comics Rate:',
            'comics_rate9':'151-200 Comics Rate:',
            'comics_rate10':'201-300 Comics Rate:',
        }
        widgets = {
            'country': forms.Select(attrs={'class': u'form-control', 'disabled': u'true',}),
#            'comics_rate1': TextInput(attrs={
#                 'class': u'form-control mb-lg',
#                 'placeholder': u'Rate'
#             }),
        }
