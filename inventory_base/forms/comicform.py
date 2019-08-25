from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['cover','age','is_cgc_rated', 'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', 'price', 'section','price','cost', 'store',]
        labels = {
            'cover': 'Image',
            'is_cgc_rated': 'CGC Rated',
            'cgc_rating': 'CGC Rating',
            'label_colour': 'Label Colour',
            'condition_rating': 'Condition Rating',
            'is_canadian_priced_variant': 'Is Canadian Priced Variant',
            'is_variant_cover': 'Is Variant Cover',
            'is_retail_incentive_variant': 'Is Retail Incentive Variant',
        }
        widgets = {
            'age': forms.Select(attrs={'class': u'form-control mb10 mt-lg'}),
            'cgc_rating': forms.Select(attrs={'class': u'form-control'}),
            'label_colour': forms.Select(attrs={'class': u'form-control m0 mb10'}),
            'condition_rating': forms.Select(attrs={'class': u'form-control m0 mb10'}),
            'price': forms.NumberInput(attrs={'class': u'form-control mb10','placeholder': u'Price Amount'}),
            'cost': forms.NumberInput(attrs={'class': u'form-control mb10','placeholder': u'Cost Amount'}),
            'location': forms.Select(attrs={'class': u'form-control m0 mb10'}),
            'section': forms.Select(attrs={'class': u'form-control m0 mb10'}),
            'store': forms.Select(attrs={'class': u'form-control m0 mb10'}),
        }
