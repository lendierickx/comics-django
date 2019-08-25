import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist
from inventory_base.forms.customerform import CustomerForm
from inventory_setting.forms.userform import UserForm


def authentication_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
    # Redirect the user to a forbidden error if the store or organization
    # are not listed.
    if org:
        if org.is_listed is False:
            return HttpResponseRedirect("/403")
    if store:
        if store.is_listed is False:
            return HttpResponseRedirect("/403")
    
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
    return render(request, 'store_customer/authentication/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'my_account',
    })


@login_required(login_url='/customer/authentication')
def my_account_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/my_account/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'my_account',
    })


@login_required(login_url='/customer/authentication')
def order_history_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
    # Fetch required data.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Fetch Order List
    try:
        all_receipts = Receipt.objects.filter(customer=customer)
    except Receipt.DoesNotExist:
        all_receipts = None
    
    # Display the view with all our model information.
    return render(request, 'store_customer/order_history/master.html',{
        'all_receipts': all_receipts,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'order_history',
        'NEW_ORDER_STATUS': constants.NEW_ORDER_STATUS,
        'PICKED_STATUS': constants.PICKED_STATUS,
        'SHIPPED_STATUS': constants.SHIPPED_STATUS,
        'RECEIVED_STATUS': constants.RECEIVED_STATUS,
        'IN_STORE_SALE_STATUS': constants.IN_STORE_SALE_STATUS,
        'ONLINE_SALE_STATUS': constants.ONLINE_SALE_STATUS,
        'CASH_PAYMENT_METHOD': constants.CASH_PAYMENT_METHOD,
        'DEBIT_CARD_PAYMENT_METHOD': constants.DEBIT_CARD_PAYMENT_METHOD,
        'CREDIT_CARD_PAYMENT_METHOD': constants.CREDIT_CARD_PAYMENT_METHOD,
        'GIFT_CARD_PAYMENT_METHOD': constants.GIFT_CARD_PAYMENT_METHOD,
        'STORE_POINTS_PAYMENT_METHOD': constants.STORE_POINTS_PAYMENT_METHOD,
        'CHEQUE_PAYMENT_METHOD': constants.CHEQUE_PAYMENT_METHOD,
        'PAYPAL_PAYMENT_METHOD': constants.PAYPAL_PAYMENT_METHOD,
        'INVOICE_PAYMENT_METHOD': constants.INVOICE_PAYMENT_METHOD,
        'OTHER_PAYMENT_METHOD': constants.OTHER_PAYMENT_METHOD,
    })


@login_required(login_url='/customer/authentication')
def order_details_page(request, receipt_id=0):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch required data.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)
    wishlists = Wishlist.objects.filter_by_customer_id_or_none(customer.customer_id)
    
    # Fetch Specific Order
    try:
        this_receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        this_receipt = None
    
    # Display the view with all our model information.
    return render(request, 'store_customer/order_history/detail.html',{
        'this_receipt': this_receipt,
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'order_history',
        'NEW_ORDER_STATUS': constants.NEW_ORDER_STATUS,
        'PICKED_STATUS': constants.PICKED_STATUS,
        'SHIPPED_STATUS': constants.SHIPPED_STATUS,
        'RECEIVED_STATUS': constants.RECEIVED_STATUS,
        'IN_STORE_SALE_STATUS': constants.IN_STORE_SALE_STATUS,
        'ONLINE_SALE_STATUS': constants.ONLINE_SALE_STATUS,
        'CASH_PAYMENT_METHOD': constants.CASH_PAYMENT_METHOD,
        'DEBIT_CARD_PAYMENT_METHOD': constants.DEBIT_CARD_PAYMENT_METHOD,
        'CREDIT_CARD_PAYMENT_METHOD': constants.CREDIT_CARD_PAYMENT_METHOD,
        'GIFT_CARD_PAYMENT_METHOD': constants.GIFT_CARD_PAYMENT_METHOD,
        'STORE_POINTS_PAYMENT_METHOD': constants.STORE_POINTS_PAYMENT_METHOD,
        'CHEQUE_PAYMENT_METHOD': constants.CHEQUE_PAYMENT_METHOD,
        'PAYPAL_PAYMENT_METHOD': constants.PAYPAL_PAYMENT_METHOD,
        'INVOICE_PAYMENT_METHOD': constants.INVOICE_PAYMENT_METHOD,
        'OTHER_PAYMENT_METHOD': constants.OTHER_PAYMENT_METHOD,
    })


@login_required(login_url='/customer/authentication')
def wishlist_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/wishlist/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })


@login_required(login_url='/customer/authentication')
def my_address_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/my_address/master.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })


@login_required(login_url='/customer/authentication')
def billing_address_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/my_address/detail_bill.html',{
        'form': CustomerForm(instance=customer),
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })


@login_required(login_url='/customer/authentication')
def shipping_address_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/my_address/detail_ship.html',{
        'form': CustomerForm(instance=customer),
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })

@login_required(login_url='/customer/authentication')
def personal_info_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/personal_info/view.html',{
        'customer_form': CustomerForm(instance=customer),
        'user_form': UserForm(instance=customer),
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })


@login_required(login_url='/customer/authentication')
def change_password_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store
    
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
    return render(request, 'store_customer/password/view.html',{
        'customer_form': CustomerForm(instance=customer),
        'user_form': UserForm(instance=customer),
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'wishlist',
    })