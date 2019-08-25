import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.catalog_item import CatalogItem
from inventory_catalog.forms import CatalogItemForm

@login_required(login_url='/inventory/login')
def catalog_page(request, org_id, store_id):
    try:
        catalog_items = CatalogItem.objects.filter(organization_id=org_id,store_id=store_id)
    except CatalogItem.DoesNotExist:
        catalog_items = None
    return render(request, 'inventory_catalog/list/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'catalog_items': catalog_items,
        'tab':'catalog_list_all',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def catalog_add_page(request, org_id, store_id):
    return render(request, 'inventory_catalog/add/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': CatalogItemForm(),
        'tab':'catalog_add',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def catalog_edit_page(request, org_id, store_id, catalog_id):
    try:
        catalog_item = CatalogItem.objects.get(catalog_id=catalog_id)
    except CatalogItem.DoesNotExist:
        catalog_item = None
    return render(request, 'inventory_catalog/edit/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': CatalogItemForm(instance=catalog_item),
        'tab':'catalog_edit',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })