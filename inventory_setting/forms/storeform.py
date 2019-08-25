from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.imageupload import ImageUpload
from api.models.ec.store import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'street_name', 'street_number', 'unit_number', 'city' , 'province' , 'country' , 'postal' , 'website' , 'email' , 'phone' , 'fax' , 'is_open_monday' , 'is_open_tuesday', 'is_open_wednesday', 'is_open_thursday', 'is_open_friday', 'is_open_saturday', 'is_open_sunday', 'monday_to', 'tuesday_to', 'wednesday_to', 'thursday_to', 'friday_to', 'saturday_to', 'sunday_to', 'monday_from', 'tuesday_from', 'wednesday_from', 'thursday_from', 'friday_from', 'saturday_from', 'sunday_from', 'currency', 'language', 'tax_rate', 'is_comics_vendor', 'is_furniture_vendor', 'is_coins_vendor', 'is_aggregated', 'paypal_email', 'style', 'is_listed',
                  ]
        labels = {
            'tax_rate': 'Tax Percent',
            'is_aggregated': 'Listed in Aggregate Store',
        }
        widgets = {
           'name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Store Name'
            }),
            'description': Textarea(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Description',
                'style':'height:100px;',
            }),
            'street_number': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street #'
            }),
            'street_name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street Name'
            }),
            'unit_number': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Unit #'
            }),
            'city': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter City'
            }),
            'province': forms.Select(attrs={'class': u'form-control'}),
            'country': forms.Select(attrs={'class': u'form-control'}),
            'postal': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Postal Code / Zip'
            }),
            'website': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Website URL'
            }),
            'email': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Email Address'
            }),
            'phone': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Phone Number'
            }),
            'fax': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Fax Number'
            }),
            'facebook_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Facebook URL'
            }),
            'twitter': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Twitter URL'
            }),
            'instagram_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Instagram URL'
            }),
            'linkedin_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter LinkedIn URL'
            }),
            'github_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter GitHub URL'
            }),
            'google_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Google+ URL'
            }),
            'youtube_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter YouTube URL'
            }),
            'flickr_url': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Flicker URL'
            }),
            'monday_to': forms.Select(attrs={'class': u'form-control'}),
            'tuesday_to': forms.Select(attrs={'class': u'form-control'}),
            'wednesday_to':forms.Select(attrs={'class': u'form-control'}),
            'thursday_to': forms.Select(attrs={'class': u'form-control'}),
            'friday_to': forms.Select(attrs={'class': u'form-control'}),
            'saturday_to': forms.Select(attrs={'class': u'form-control'}),
            'sunday_to': forms.Select(attrs={'class': u'form-control'}),
            'monday_from': forms.Select(attrs={'class': u'form-control'}),
            'tuesday_from': forms.Select(attrs={'class': u'form-control'}),
            'monday_to': forms.Select(attrs={'class': u'form-control'}),
            'wednesday_from':forms.Select(attrs={'class': u'form-control'}),
            'thursday_from': forms.Select(attrs={'class': u'form-control'}),
            'friday_from': forms.Select(attrs={'class': u'form-control'}),
            'saturday_from': forms.Select(attrs={'class': u'form-control'}),
            'sunday_from': forms.Select(attrs={'class': u'form-control'}),
            'currency': forms.Select(attrs={'class': u'form-control'}),
            'language': forms.Select(attrs={'class': u'form-control'}),
            'tax_rate': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Tax Rate'
            }),
#            'is_comics_vendor': forms.Select(attrs={'class': u'form-control'}),
#            'is_furniture_vendor': forms.Select(attrs={'class': u'form-control'}),
#            'is_coins_vendor': forms.Select(attrs={'class': u'form-control'}),
            'paypal_email': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter PayPal Email Address'
            }),
            'style': forms.Select(attrs={'class': u'form-control'}),
    }
