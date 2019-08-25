import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.tag import Tag
from inventory_products.forms import ComicForm
from inventory_products.forms import ProductForm


@login_required(login_url='/inventory/login')
def search_comics_page(request, org_id, store_id):
    store = Store.objects.get(store_id=store_id)
    
    try:
        tags = Tag.objects.filter(organization__org_id=org_id)
    except Tag.DoesNotExist:
        tags = None
    try:
        sections = Section.objects.filter(store=store)
    except Section.DoesNotExist:
        sections = None
    
    stores = Store.objects.filter(organization_id=org_id, is_suspended=False)
    product_form = ProductForm(initial={'price': 5.00})
    product_form.fields["store"].queryset = stores
    product_form.fields["section"].queryset = sections

    return render(request, 'inventory_products/comic/search_gcd/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': store,
        'tags': tags,
        'comic_form': ComicForm(),
        'product_form': product_form,
        'tab':'add',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
        'src_urls': ['inventory_products/comic/search_gcd/modal.html'],
    })


@login_required(login_url='/inventory/login')
def search_products_page(request, org_id, store_id):
    return render(request, 'inventory_products/comic/search_ec/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'prduct_comics',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })