import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ecantina_project import constants
from inventory_base.forms.imageuploadform import ImageUploadForm
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm


def registration_step1_page(request):
    return render(request, 'store_register/step1/view.html',{
        'org': request.organization,
        'store': request.store,
        'user_form': UserForm(),
        'page' : 'register',
    })


def registration_step2_page(request):
    return render(request, 'store_register/step2/view.html',{
        'org': request.organization,
        'store': request.store,
        'user_form': UserForm(),
        'page' : 'register',
    })


@login_required(login_url='/store/register/step1')
def registration_step3_page(request):
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    return render(request, 'store_register/step3/view.html',{
        'org': request.organization,
        'store': request.store,
        'customer': customer,
        'customer_form': CustomerForm(instance=customer),
        'page' : 'register',
    })


@login_required(login_url='/store/register/step1')
def registration_step4_page(request):
    organization = request.organization
    store = request.store
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    return render(request, 'store_register/step4/view.html',{
        'org': organization,
        'store': store,
        'customer': customer,
        'customer_form': CustomerForm(instance=customer),
        'page' : 'register',
    })


@login_required(login_url='/store/register/step1')
def registration_step5_page(request):
    organization = request.organization
    store = request.store
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    return render(request, 'store_register/step5/view.html',{
        'org': organization,
        'store': store,
        'customer': customer,
        'customer_form': CustomerForm(instance=customer),
        'page' : 'register',
        'src_urls': ['store_register/step5/success_modal.html'], # MODAL
    })