from datetime import date
from django.db import models
from django import forms
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic


class IssueForm(forms.Form):
    series = forms.CharField(
        label='Series',
        max_length=100,
        widget=forms.forms.TextInput(attrs={
            'class':'form-control mb10 input-disabled mt0 p0',
            'style':'position:relative;top:-3px;',
            'placeholder':'Series',
            'readonly': u'true',
        }),
    )

    number = forms.CharField(
        label='Issue #',
        max_length=100,
        widget=forms.forms.TextInput(attrs={
            'class':'form-control mb10 input-disabled p0',
            'placeholder':'Issue #','readonly': u'true',
        }),
    )

    title = forms.CharField(
        label='Comic Title',
        max_length=100,
        widget=forms.forms.TextInput(attrs={
            'class':'form-control mb10 input-disabled p0',
            'placeholder':'Comic Title','readonly': u'true',
        }),
    )

    publisher = forms.CharField(
        label='Publisher Name',
        max_length=100,
        widget=forms.forms.TextInput(attrs={
            'class':'form-control mb10 input-disabled p0','placeholder':'Publisher Name','readonly': u'true',
        }),
    )

    genre = forms.CharField(
        label='Genre',
        max_length=100,
        widget=forms.forms.TextInput(attrs={
            'class':'form-control mb10 input-disabled p0','placeholder':'Genre','readonly': u'true',
        }),
    )
