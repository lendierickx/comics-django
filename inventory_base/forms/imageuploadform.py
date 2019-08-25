from datetime import date
from django.db import models
from django import forms
from django.forms.widgets import EmailInput
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
