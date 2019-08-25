import json
from datetime import datetime
from decimal import *
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.product import Product
from api.models.ec.receipt import Receipt


@login_required(login_url='/inventory/login')
def checkout_page(request, org_id, store_id, receipt_id):
    return render(request, 'inventory_checkout/item/index.html',{
        'today': str(datetime.now()),
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'receipt': Receipt.objects.get(receipt_id=receipt_id),
        'tab':'checkout',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })


@login_required(login_url='/inventory/login')
def content_page(request, org_id, store_id, receipt_id):
    # Note: If you want to know how to handle decimal places and rounding
    #       then checkout this URL:
    #       https://docs.python.org/3/library/decimal.html#decimal-faq
    
    store = Store.objects.get(store_id=store_id)
    receipt = Receipt.objects.get(receipt_id=receipt_id)
    sub_total_amount = Decimal(0.00)
    total_amount = Decimal(0.00)
    total_tax = Decimal(0.00)
    
    for product in receipt.products.all():
        sub_total_amount += Decimal(product.price)
        if receipt.has_tax:
           total_tax += Decimal(store.tax_rate) * Decimal(product.price)
    total_amount = Decimal(sub_total_amount) + Decimal(total_tax)

    TWOPLACES = Decimal(10) ** -2       # same as Decimal('0.01')
    return render(request, 'inventory_checkout/item/content.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'receipt': receipt,
        'sub_total_amount': sub_total_amount.quantize(TWOPLACES),
        'tax': Decimal(store.tax_rate) * Decimal(100.00),
        'total_tax': total_tax.quantize(TWOPLACES),
        'total_amount': total_amount.quantize(TWOPLACES),
        'employee': Employee.objects.get(user__id=request.user.id),
    })


@login_required()
def ajax_change_discount_type(request, org_id, store_id, receipt_id, product_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                product = Product.objects.get(product_id=int(product_id))
                
                # Reset amounts.
                product.discount = 0.00
                product.price = product.sub_price
                
                # Switch discount type
                if product.discount_type is 1: # Percent
                    product.discount_type = 2
                elif product.discount_type is 2: # Amount
                    product.discount_type = 1
                
                # Save changes and return success.
                product.save()
                response_data = {'status': 'success','message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_change_discount_amount(request, org_id, store_id, receipt_id, product_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                product = Product.objects.get(product_id=int(product_id))
                discount = request.POST['discount']
                if product.discount_type is 1: # Percent
                    product.discount = discount
                    rate = Decimal(discount) / Decimal(100)
                    discount = Decimal(rate) * Decimal(product.sub_price)
                elif product.discount_type is 2: # Amount
                    product.discount = discount
                product.price = Decimal(product.sub_price) - Decimal(discount)
                product.save()
                response_data = {'status': 'success', 'message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def ajax_change_tax(request, org_id, store_id, receipt_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                receipt = Receipt.objects.get(receipt_id=int(receipt_id))
                receipt.has_tax = not receipt.has_tax
                receipt.save()
                response_data = {'status': 'success', 'message': 'changed',}
            except Product.DoesNotExist:
                response_data = {'status': 'failed','message': 'product does not exist',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
