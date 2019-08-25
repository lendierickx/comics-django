from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'street_name', 'street_number', 'unit_number', 'city' , 'province' , 'country' , 'postal' , 'website' , 'email' , 'phone' , 'fax' , 'twitter' , 'facebook_url' , 'currency', 'language', 'paypal_email', 'style', 'is_listed',
#                  'instagram_url' , 'linkedin_url' , 'github_url' , 'google_url' , 'youtube_url' , 'flickr_url'
                  ]
        labels = {

        }
        widgets = {
           'name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Organization Name'
           }),
           'description': Textarea(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Description',
                'style':'height:100px;',
            }),
            'street_number': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Street #'
            }),
            'street_name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Street Name'
            }),
            'unit_number': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Unit #'
            }),
            'city': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter City'
            }),
            'province': forms.Select(attrs={'class': u'form-control'}),
            'country': forms.Select(attrs={'class': u'form-control'}),
            'postal': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Postal Code / Zip'
            }),
            'website': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Website URL'
            }),
            'email': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Email Address'
            }),
            'phone': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Phone Number'
            }),
            'fax': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Fax Number'
            }),
            'facebook_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Facebook URL, Ex.: https://www.facebook.com/LuchaComics'
            }),
            'twitter': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Twitter Hashtag, Ex.: LuchaComics'
            }),
            'instagram_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Instagram URL'
            }),
            'linkedin_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter LinkedIn URL'
            }),
            'github_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter GitHub URL'
            }),
            'google_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Google+ URL'
            }),
            'youtube_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter YouTube URL'
            }),
            'flickr_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Flicker URL'
            }),
            'currency': forms.Select(attrs={'class': u'form-control'}),
            'language': forms.Select(attrs={'class': u'form-control'}),
            'paypal_email': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter PayPal Receiving Email Address'
            }),
           'style': forms.Select(attrs={'class': u'form-control'}),
        }
