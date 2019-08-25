import json
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product


@login_required(login_url='/inventory/login')
def checkout_page(request, org_id, store_id, receipt_id):
    store = Store.objects.get(store_id=store_id)
    tax = Decimal(store.tax_rate) * Decimal(100.00)
    return render(request, 'inventory_checkout/receipt/index.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': store,
        'tax': tax,
        'receipt': Receipt.objects.get(receipt_id=receipt_id),
        'tab':'checkout',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })