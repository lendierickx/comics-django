import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def front_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Fetch all the featured comics throughout all the stores or depending
    # on the organization / store.
    try:
        featured_products = Product.objects.filter(
            is_listed=True,
            store__is_aggregated=True,
            is_sold=False,
            is_featured=True,
            organization__is_listed=True,
            store__is_listed=True,
        )
    
        if org:
            featured_products = featured_products.filter(organization=org).order_by('-price')
                
        if store:
            featured_products = featured_products.filter(store=store).order_by('-price')
    except Product.DoesNotExist:
        featured_products = None
    
    # Fetch all the new comics throghout all the stores or depending on the
    # organization / store.
    try:
        new_products = Product.objects.filter(
            is_listed=True,
            store__is_aggregated=True,
            is_sold=False,
            is_new=True,
        )

        if org:
            new_products = new_products.filter(organization=org)

        if store:
            new_products = new_products.filter(store=store)
    except Product.DoesNotExist:
        new_products = None

    # Display the view with all our model information.
    return render(request, 'store_landpage/index.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'featured_products': featured_products,
        'new_products': new_products,
        'org': org,
        'store': store,
        'page': 'home',
        'settings': settings,
    })


def tos_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists

    # Display the view with all our model information.
    return render(request, 'store_landpage/tos.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def privacy_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    customer = request.customer
    receipt = request.receipt
    wishlists = request.wishlists
    
    # Display the view with all our model information.
    return render(request, 'store_landpage/privacy.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


