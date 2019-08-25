from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.category import Category


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['age','is_cgc_rated', 'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', ]
        labels = {
            'is_cgc_rated': 'CGC Rated',
            'cgc_rating': 'CGC Rating',
            'label_colour': 'Label Colour',
            'condition_rating': 'Condition Rating',
            'is_canadian_priced_variant': 'Is Canadian Priced Variant',
            'is_variant_cover': 'Is Variant Cover',
            'is_retail_incentive_variant': 'Is Retail Incentive Variant',
        }
        widgets = {
            'age': forms.Select(attrs={'class': u'form-control'}),
            'cgc_rating': forms.Select(attrs={'class': u'form-control'}),
            'label_colour': forms.Select(attrs={'class': u'form-control m0 mb10'}),
            'condition_rating': forms.Select(attrs={'class': u'form-control m0 mb10'}),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = GCDIssue
        fields = ['series','number', 'title', 'publisher_name', 'genre', ]
        labels = {
            'series': 'Series',
            'number': 'Issue #',
            'title': 'Comic Title',
            'publisher_name': 'Publisher',
            'genre': 'Genre',
        }
        widgets = {
            'series': forms.TextInput(attrs={
                'class': u'form-control mb10 input-disabled mt0 p0',
                'style':'position:relative;top:-3px;',
                'placeholder':'Series',
                'readonly': u'true',
            }),
            'number': forms.TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Issue #','readonly': u'true',
            }),
            'title': forms.TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Comic Title','readonly': u'true',
            }),
            'publisher_name': forms.TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Publisher Name','readonly': u'true',
            }),
            'genre': forms.TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Genre','readonly': u'true',
            }),
        }


from datetime import date
from django.db import models
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from api.models.ec.imageupload import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        labels = {

        }
        widgets = {

    }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'section', 'sub_price','price','cost', 'store','type','images', 'category', 'qrcode', 'has_no_shipping', 'is_listed', 'is_new', 'is_featured',]
        labels = {

        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Product Name',
            }),
            'description': forms.Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'images': forms.Select(attrs={'class': u'form-control mb10 mt-lg'}),
            'type': forms.Select(attrs={'class': u'form-control'}),
            'sub_price': forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Price Amount', 'step': 1.00}),
            'price': forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Price Amount', 'step': 1.00}),
            'cost': forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Cost Amount', 'step': 1.00}),
            'location': forms.Select(attrs={'class': u'form-control'}),
            'section': forms.Select(attrs={'class': u'form-control'}),
            'store': forms.Select(attrs={'class': u'form-control'}),
            'category': forms.Select(attrs={'class': u'form-control'}),
    }
