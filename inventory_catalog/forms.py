from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.catalog_item import CatalogItem


class CatalogItemForm(forms.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ['name', 'type', 'description', 'brand_name', 'image', 'length_in_meters','width_in_meters', 'height_in_meters','weight_in_kilograms','volume_in_litres','materials', 'is_tangible', 'is_flammable', 'is_biohazard', 'is_toxic', 'is_explosive', 'is_corrosive', 'is_volatile', 'is_radioactive', 'is_restricted','restrictions','organization','store',]
        labels = {
            'length_in_meters': 'Length (m)',
            'width_in_meters': 'Width (m)',
            'height_in_meters': 'Height (m)',
            'weight_in_kilograms': 'Weight (kg)',
            'volume_in_litres': 'Volume (L)',
        }
        widgets = {
            'type': forms.Select(attrs={'class': u'form-control'}),
            'name': forms.TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Name of Item'
            }),
            'description': forms.Textarea(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Description',
                'style':'height:100px;',
            }),
            'brand_name': forms.TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Brand Name of Item'
            }),
        }
