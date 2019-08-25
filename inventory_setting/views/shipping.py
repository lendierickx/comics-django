import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from inventory_setting.forms.org_shipping_preference_form import OrgShippingPreferenceForm
from inventory_setting.forms.org_shipping_rates_form import OrgShippingRateForm


@login_required(login_url='/inventory/login')
def shipping_settings_page(request, org_id, store_id):
    # Get our organization preferences.
    try:
        org_preference = OrgShippingPreference.objects.get(organization_id=org_id)
    except OrgShippingPreference.DoesNotExist:
        org_preference = OrgShippingPreference.objects.create(
            organization_id = org_id,
        )

    return render(request, 'inventory_setting/shipping/master.html',{
        'org_form': OrgShippingPreferenceForm(instance=org_preference),
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'employee': Employee.objects.get(user__id=request.user.id),
        'tab':'shipping_settings',
        'locations': Store.objects.filter(organization_id=org_id),
    })

@login_required(login_url='/inventory/login')
def shipping_details_settings_page(request, org_id, store_id, shipping_rate_id=0):
    # Get our organization preferences.
    try:
        org_preference = OrgShippingPreference.objects.get(organization_id=org_id)
    except OrgShippingPreference.DoesNotExist:
        org_preference = OrgShippingPreference.objects.create(organization_id = org_id,)
    
    try:
        rate = OrgShippingRate.objects.get(shipping_rate_id=shipping_rate_id)
    except OrgShippingRate.DoesNotExist:
        rate = None

    return render(request, 'inventory_setting/shipping/details.html',{
        'org_preference': org_preference,
        'form': OrgShippingRateForm(instance=rate),
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'employee': Employee.objects.get(user__id=request.user.id),
        'tab':'shipping_settings',
        'locations': Store.objects.filter(organization_id=org_id),
    })