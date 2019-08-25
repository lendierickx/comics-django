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
from django.views.decorators.http import last_modified


def last_updated(request, org_id, store_id):
    return Organization.objects.get(org_id=org_id).last_updated


@last_modified(last_updated)
@login_required(login_url='/inventory/login')
def org_settings_page(request, org_id, store_id):
    employee = Employee.objects.get(user__id=request.user.id)
    form = OrganizationForm(instance=employee.organization)
    logo = employee.organization.logo
    return render(request, 'inventory_setting/org/view.html',{
        'org': employee.organization,
        'store': Store.objects.get(store_id=store_id),
        'upload_id': 0 if logo is None else logo.upload_id,
        'tab':'org_settings',
        'employee': employee,
        'form': form,
        'user_form': UserForm(instance=request.user), # Note: Possibly might error
        'locations': Store.objects.filter(organization_id=org_id),
    })