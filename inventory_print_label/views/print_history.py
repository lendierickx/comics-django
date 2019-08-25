import os
import json
import qrcode
from PIL import Image
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product
from api.models.ec.comic import Comic
from api.models.ec.print_history import PrintHistory


@login_required(login_url='/inventory/login')
def print_history_page(request, org_id, store_id):
    try:
        history = PrintHistory.objects.filter(store_id=store_id)
    except PrintHistory.DoesNotExist:
        history = None
    return render(request, 'inventory_print_label/print_history/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'history': history,
        'tab':'print',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })