import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.tag import Tag
from api.models.ec.promotion import Promotion
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def list_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    organization = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Fetch objects used for searching criteria.
    try:
        categories = Category.objects.all().order_by('category_id')
    except Category.DoesNotExist:
        categories = None

    try:
        brands = Brand.objects.all()
    except Brand.DoesNotExist:
        brands = None

    # Get the categories and select the current category.
    try:
        category_id = int(request.GET.get('category'))
    except Exception as e:
        category_id = 1  # Automatically set to "All Comics".

    try:
        current_category = Category.objects.get(category_id=category_id)
    except Category.DoesNotExist:
        current_category = None

    return render(request, 'store_products/product_list/list.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'categories': categories,
        'current_category': current_category,
        'brands': brands,
        'brand_name': request.GET.get('brand_name'),
        'org': organization,
        'store': store,
        'page' : 'products',
    })
