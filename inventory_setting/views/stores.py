import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.section import Section
from inventory_setting.forms.storeform import StoreForm
from inventory_setting.forms.organizationform import OrganizationForm
from inventory_setting.forms.userform import UserForm
from inventory_setting.forms.sectionform import SectionForm
from inventory_setting.forms.employeeform import EmployeeForm


@login_required(login_url='/inventory_login')
def edit_store_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    this_store = Store.objects.get(store_id=this_store_id)
    
    # Return all the stores belonging to this organization EXCEPT
    # the main store we are logged in as.
    #stores =  Store.objects.filter(organization=organization)
    #stores =  stores.filter(~Q(store_id = this_store_id))
    return render(request, 'inventory_setting/store/edit/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': this_store,
        'stores': Store.objects.filter(organization=organization),
        'sections': Section.objects.filter(store=this_store),
        'tab':'store_settings',
        'employee': Employee.objects.get(user__id=request.user.id),
        'form': StoreForm(instance=this_store),
        'locations': Store.objects.filter(organization_id=org_id),
    })


# Stores - Add
#--------------


@login_required(login_url='/inventory_login')
def store_settings_page(request, org_id, store_id):
    organization = Organization.objects.get(org_id=org_id)
    store = Store.objects.get(store_id=store_id)
    return render(request, 'inventory_setting/store/add/view.html',{
        'org': organization,
        'store': store,
        'stores': Store.objects.filter(organization=organization),
        'sections': Section.objects.filter(store=store),
        'tab':'store_settings',
        'employee': Employee.objects.get(user__id=request.user.id),
        'form': StoreForm(),
        'locations': Store.objects.filter(organization_id=org_id),
    })
