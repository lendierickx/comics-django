import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.gcd.story import GCDStory
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def details_page(request, product_id=0):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    organization = request.organization
    store = request.store
    product_id = int(product_id)
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Fetch objects used for searching criteria.
    try:
        categories = Category.objects.all().order_by('category_id')
    except Category.DoesNotExist:
        categories = None

    # Fetch the product details & stories.
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        product = None
    try:
        comic = Comic.objects.get(product__product_id=product_id)
        stories = GCDStory.objects.filter(issue_id=comic.issue_id)
    except Comic.DoesNotExist:
        comic = None
        stories = None
    except GCDStory.DoesNotExist:
        comic = None
        stories = None

    return render(request, 'store_products/product_details/details.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': organization,
        'store': store,
        'categories': categories,
        'comic': comic,
        'stories': stories,
        'product': product,
    })
