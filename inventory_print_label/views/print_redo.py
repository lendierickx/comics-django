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


@login_required(login_url='/inventory/login')
def comics_redo_page(request, org_id, store_id):
    # Fetch all the comics starting with the most recent submission
    # grouped by comic series.
    q = Comic.objects.filter(
        product__store_id=store_id,
        product__is_qrcode_printed=True,
        product__is_sold=False,
    )
    q = q.order_by('issue__series')
    q.query.group_by = ['issue__series']

    paginator = Paginator(q, 100) # Show 100 comics per page
    page = request.GET.get('page')
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comics = paginator.page(paginator.num_pages)
    return render(request, 'inventory_print_label/print_redo/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'comics': comics,
        'tab':'print',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })