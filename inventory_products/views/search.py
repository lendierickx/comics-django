import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.story import GCDStory
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.product import Product

@login_required(login_url='/inventory/login')
def product_search_page(request, org_id, store_id):
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        categories = None

    try:
        brands = Brand.objects.all()
    except Brand.DoesNotExist:
        brands = None

    return render(request, 'inventory_products/search/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'search_products',
        'categories': categories,
        'brands': brands,
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })