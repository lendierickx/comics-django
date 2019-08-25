import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist
from api.models.ec.subdomain import SubDomain
from ecantina_project.settings import env_var


def http_403_page(request):
    org_id = 0
    store_id = 0
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)

    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)

    # Display the view with all our model information.
    return render(request, 'store_base/403.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def http_404_page(request):
    org_id = 0
    store_id = 0
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)

    # Fetch the Organization / Store.
    org = Organization.objects.get_or_none(org_id)
    store = Store.objects.get_or_none(store_id)

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    wishlists = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)
        wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)

    # Display the view with all our model information.
    return render(request, 'store_base/403.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'tos',
    })


def storefront_redirect(request, name=""):
    """
        Function will lookup the domain name and redirect the user to
        the respected storefront at the particular sub-domain.
    """
    # Find the subdomain associated with this organization.
    try:
        this_subdomain = SubDomain.objects.get(name=name)
    except SubDomain.DoesNotExist:
        return HttpResponseRedirect("/404")

    url = env_var('HTTP_PROTOCOL')+this_subdomain.name+"."+env_var('DOMAIN')
    return HttpResponseRedirect(url)


def org_subdomain_redirect(request, org_id=0):
    """
        Example:
        127.0.0.1:8000/store/directory/1/
        """
    org_id = int(org_id)
    # Find the subdomain associated with this organization.
    try:
        this_subdomain = SubDomain.objects.filter(organization=org_id).order_by("-store")[:1]
        this_subdomain = this_subdomain[0]
    except SubDomain.DoesNotExist:
        this_subdomain = None

    url = env_var('HTTP_PROTOCOL')+this_subdomain.name+"."+env_var('DOMAIN')
    return HttpResponseRedirect(url)


def store_subdomain_redirect(request, org_id=0, store_id=0):
    org_id = int(org_id)
    store_id = int(store_id)

    # Find the subdomain associated with this store.
    try:
        this_subdomain = SubDomain.objects.get(store_id=store_id)
    except SubDomain.DoesNotExist:
        this_subdomain = None

    url = env_var('HTTP_PROTOCOL')+this_subdomain.name+"."+env_var('DOMAIN')
    return HttpResponseRedirect(url)
