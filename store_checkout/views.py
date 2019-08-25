import json
from datetime import datetime
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ecantina_project import constants
from ecantina_project.settings import env_var
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from inventory_base.forms.customerform import CustomerForm
from inventory_base.forms.readonlycustomerform import ReadOnlyCustomerForm


# Import our signals.
from store_checkout.signlas import *


def cart_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # If user is logged in, fetch the Customer record or create one. Then
    # fetch a Receipt record or create a new one.
    customer = None
    receipt = None
    if request.user.is_authenticated():
        customer = Customer.objects.get_or_create_for_user_email(request.user.email)
        receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/cart/view.html',{
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'home',
    })


@login_required(login_url='/')
def checkout_shipping_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping/view.html',{
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'form': ReadOnlyCustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_billing_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/billing/view.html',{
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'form': ReadOnlyCustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_shipping_method_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/shipping_method/view.html',{
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


@login_required(login_url='/')
def checkout_payment_method_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/payment_method/view.html',{
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


@csrf_exempt
@login_required(login_url='/')
def checkout_thank_you_page(request, receipt_id=0):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch OLD receipt and process it.
    old_receipt = Receipt.objects.get_or_none(receipt_id=receipt_id)

    # STEP 1: Update Customer information.
    billing_address = old_receipt.customer.billing_street_number
    billing_address += ' ' + old_receipt.customer.billing_street_name
    if old_receipt.customer.billing_unit_number:
        billing_address = old_receipt.customer.billing_unit_number + '-' + billing_address

    shipping_address = old_receipt.customer.shipping_street_number
    shipping_address += ' ' + old_receipt.customer.shipping_street_name
    if old_receipt.customer.shipping_unit_number:
        shipping_address = old_receipt.customer.shipping_unit_number + '-' + shipping_address

    old_receipt.email = old_receipt.customer.email
    old_receipt.billing_address = billing_address
    old_receipt.billing_phone = old_receipt.customer.billing_phone
    old_receipt.billing_city = old_receipt.customer.billing_city
    old_receipt.billing_province = old_receipt.customer.billing_province
    old_receipt.billing_country = old_receipt.customer.billing_country
    old_receipt.billing_postal = old_receipt.customer.billing_postal
    old_receipt.shipping_address = shipping_address
    old_receipt.shipping_phone = old_receipt.customer.shipping_phone
    old_receipt.shipping_city = old_receipt.customer.shipping_city
    old_receipt.shipping_province = old_receipt.customer.shipping_province
    old_receipt.shipping_country = old_receipt.customer.shipping_country
    old_receipt.shipping_postal = old_receipt.customer.shipping_postal

    # STEP 2: Finalize our receipt.
    old_receipt.purchased = datetime.today()
    old_receipt.has_finished = True
    old_receipt.status = constants.ONLINE_SALE_STATUS
    old_receipt.payment_method = constants.PAYPAL_PAYMENT_METHOD
    old_receipt.save()

    # STEP 3: Inform our products that they are sold out.
    for product in old_receipt.products.all():
        product.is_sold = True
        product.save()

    # Fetch Customer / Receipt
    # Note: Because our previous Receipt was set "has_finished" to true
    #       this will force a new cart to be opened / created here.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/thank_you/view.html',{
        'old_receipt': old_receipt,
        'receipt': receipt,
        'customer': customer,
        'employee': employee,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


@csrf_exempt
@login_required(login_url='/')
def checkout_cancel_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Display the view with all our model information.
    return render(request, 'store_checkout/cancel/view.html',{
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
    })


def get_paypal_currency_code(iso_currency_code):
    """
        Function will map the currency code to paypal currency code
    """
    if iso_currency_code == 124:
        return 'CAD'
    if iso_currency_code == 840:
        return 'USD'
    if iso_currency_code == 484:
        return 'MXN'
    return 'CAD'


@login_required(login_url='/')
def checkout_order_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    org = request.organization
    store = request.store

    # Fetch Customer / Receipt.
    customer = Customer.objects.get_or_create_for_user_email(request.user.email)
    receipt = Receipt.objects.get_or_create_for_online_customer(customer)

    # Generate our URLs & pick the payment email
    base_url = env_var("HTTP_PROTOCOL")
    prefix = request.META.get("HTTP_X_CUSTOMURL")

    # Configure which PayPal address to send money
    paypal_email = settings.PAYPAL_RECEIVER_EMAIL
    currency_code = 'CAD'
    if org is not None and store is None:
        paypal_email = org.paypal_email
        currency_code = get_paypal_currency_code(org.currency)
    if org is not None and store is not None:
        paypal_email = store.paypal_email
        currency_code = get_paypal_currency_code(store.currency)

    # Append the subdomain (including 'www') to the URL
    if prefix:
        base_url += prefix + "." +  env_var("DOMAIN")
    else:
        base_url += env_var("DOMAIN")

    return_url = base_url+"/checkout/thank_you/"+str(receipt.receipt_id)
    cancel_url = base_url+"/checkout/cancel"
    notify_url = env_var("HTTP_PROTOCOL") + env_var("DOMAIN") + reverse('paypal-ipn'),
    print('Pre-Checkout Receipt #', str(receipt.receipt_id))
    print('notify_url', str(notify_url))
    print('return_url', str(return_url))
    print('cancel_return', str(cancel_url))
    print('prefix', prefix)
    print("")

    # What you want the button to do.
    paypal_dict = {
        "currency_code": currency_code,
        "business": paypal_email,
        "amount": str(receipt.total_amount),
        "item_name": "Comic Book(s) Purchase, Receipt #"+str(receipt.receipt_id),
        "invoice": str(receipt.receipt_id),
        "notify_url": notify_url,
        "return": return_url,
        "return_url": return_url,
        "cancel_return": cancel_url,
        "custom": "perform_receipt_checkout",  # Custom command to correlate to some function later (optional)
    }
    form = PayPalPaymentsForm(initial=paypal_dict)

    # Run this next set of code to detect if we should give a warning to the
    # Customer so they'll know some items cannot are pickup only.
    has_no_shipping = False
    for product in receipt.products.all():
        if product.has_no_shipping:
            has_no_shipping = True

    # Display the view with all our model information.
    return render(request, 'store_checkout/order/view.html',{
#        'image_url': 'https://www.comicscantina.com/static/paypal_logo.png'  # PayPal Logo
        'has_no_shipping': has_no_shipping,
        'paypal_form': form,
        'receipt': receipt,
        'customer': customer,
        'form': CustomerForm(instance=customer),
        'org': org,
        'store': store,
        'page': 'home',
        'src_urls': ['store_checkout/order/warning_modal.html'], # MODAL
    })

# https://django-paypal.readthedocs.org/en/stable/standard/ipn.html
