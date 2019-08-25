from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.imageupload import ImageUpload
from api.models.ec.customer import Customer


class ReadOnlyCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name','billing_street_name', 'billing_street_number', 'billing_unit_number', 'billing_city' , 'billing_province' , 'billing_country' , 'billing_postal' , 'billing_phone', 'is_shipping_same_as_billing', 'shipping_street_name', 'shipping_street_number', 'shipping_unit_number', 'shipping_city' , 'shipping_province' , 'shipping_country' , 'shipping_postal' , 'shipping_phone', 'email' , 'has_consented', 'date_of_birth', 'wants_newsletter', 'wants_flyers',
        ]
        labels = {
            'has_consented': 'E-Mail Privacy Consent',
            'wants_newsletter': 'Sign up for our newsletter!',
            'wants_flyers': 'Receive special offers from our partners!',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter First Name',
                'readonly': u'true',
            }),
            'last_name': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Last Name',
                'readonly': u'true',
            }),
            'billing_street_number': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street #',
                'readonly': u'true',
            }),
            'billing_street_name': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street Name',
                'readonly': u'true',
            }),
            'billing_unit_number': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Unit #',
                'readonly': u'true',
            }),
            'billing_city': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter City',
                'readonly': u'true',
            }),
            'billing_province': forms.Select(attrs={'class': u'form-control', 'readonly': u'true',}),
            'billing_country': forms.Select(attrs={'class': u'form-control', 'readonly': u'true',}),
            'billing_postal': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Postal Code / Zip',
                'readonly': u'true',
            }),
            'billing_phone': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Phone Number',
                'readonly': u'true',
            }),
            'shipping_name': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Full Name',
                'readonly': u'true',
            }),
            'shipping_street_number': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street #',
                'readonly': u'true',
            }),
            'shipping_street_name': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street Name',
                'readonly': u'true',
            }),
            'shipping_unit_number': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Unit #',
                'readonly': u'true',
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter City',
                'readonly': u'true',
            }),
            'shipping_province': forms.Select(attrs={'class': u'form-control', 'readonly': u'true',}),
            'shipping_country': forms.Select(attrs={'class': u'form-control', 'readonly': u'true',}),
            'shipping_postal': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Postal Code / Zip',
                'readonly': u'true',
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Phone Number',
                'readonly': u'true',
            }),
            'website': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Website URL',
                'readonly': u'true',
            }),
            'email': forms.TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Email Address',
                'readonly': u'true',
            }),
            'date_of_birth': forms.SelectDateWidget(attrs={'readonly': u'true',}),
        }
