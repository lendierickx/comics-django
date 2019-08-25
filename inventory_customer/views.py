import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.pulllist import Pulllist
from api.models.ec.wishlist import Wishlist
from api.models.ec.pulllistsubscription import PulllistSubscription
from inventory_base.forms.customerform import CustomerForm


@login_required(login_url='/inventory/login')
def customers_page(request, org_id, store_id):
    return render(request, 'inventory_customer/list/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def customer_page(request, org_id, store_id, customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        form = CustomerForm(instance=customer)
    except Customer.DoesNotExist:
        customer = None
        form = CustomerForm(initial={'joined':datetime.now()})
    return render(request, 'inventory_customer/add/view.html',{
        'customer': customer,
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': form,
        'tab':'add_customer',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def profile_page(request, org_id, store_id, customer_id):
    return render(request, 'inventory_customer/profile/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'customer': Customer.objects.get(customer_id=customer_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
        'src_urls': ['inventory_customer/profile/modal.html'],
    })


@login_required(login_url='/inventory/login')
def purchases_page(request, org_id, store_id, customer_id):
    return render(request, 'inventory_customer/receipt/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'customer': Customer.objects.get(customer_id=customer_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def subscriptions_page(request, org_id, store_id, customer_id):
    # Fetch all the pullists belonging to the current client.
    try:
        subscriptions = PulllistSubscription.objects.filter(customer_id=customer_id, organization_id=org_id)
    except PulllistSubscription.DoesNotExist:
        subscriptions = None

    # Render View
    return render(request, 'inventory_customer/subscription/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'customer': Customer.objects.get(customer_id=customer_id),
        'subscriptions': subscriptions,
        'tab':'customers_list',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def wishlists_page(request, org_id, store_id, customer_id):
    # Fetch all the pullists belonging to the current client.
    try:
        wishlists = Wishlist.objects.filter(
            customer_id=customer_id,
            product__organization_id=org_id
        )
    except Wishlist.DoesNotExist:
        wishlists = None

    # Render View
    return render(request, 'inventory_customer/wishlist/view.html',{
        'wishlists': wishlists,
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'customer': Customer.objects.get(customer_id=customer_id),
        'tab':'customers_list',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })