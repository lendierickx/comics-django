from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt


def login_page(request):
    return render(request, 'mobile_pos/login.html',{
        'page':'login',
    })


@login_required(login_url='/mobile/pos/login')
def pick_store_page(request):
    try:
        employee = Employee.objects.get(user__id=request.user.id)
        stores = Store.objects.filter(organization=employee.organization)
    except Store.DoesNotExist:
        stores = None

    return render(request, 'mobile_pos/pick_store.html',{
        'stores': stores,
        'page':'pick_store',
    })


@login_required(login_url='/mobile/pos/login')
def dashboard_page(request, store_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})
    
    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipts = Receipt.objects.filter(
            has_purchased_online=False,
            has_finished=False,
            employee=employee,
        )
    except Receipt.DoesNotExist:
        receipts = None

    return render(request, 'mobile_pos/dashboard.html',{
        'store': store,
        'employee': employee,
        'receipts': receipts,
        'page': 'dashboard',
    })


@login_required(login_url='/mobile/pos/login')
def remove_product_page(request, store_id=0, receipt_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})

    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None

    return render(request, 'mobile_pos/remove_product.html',{
        'receipt': receipt,
        'store': store,
        'employee': employee,
        'page': 'cart',
    })


@login_required(login_url='/mobile/pos/login')
def cart_page(request, store_id=0, receipt_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})

    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None

    return render(request, 'mobile_pos/cart.html',{
        'receipt': receipt,
        'store': store,
        'employee': employee,
        'page': 'cart',
    })


@login_required(login_url='/mobile/pos/login')
def scanner_page(request, store_id=0, receipt_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})

    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None

    return render(request, 'mobile_pos/product_scanner.html',{
        'receipt': receipt,
        'store': store,
        'employee': employee,
        'page': 'cart',
    })


@login_required(login_url='/mobile/pos/login')
def checkout_page(request, store_id=0, receipt_id=0):
    try:
        store = Store.objects.get(store_id=store_id)
    except Store.DoesNotExist:
        return render(request, 'mobile_pos/no_store.html',{})

    employee = Employee.objects.get(user__id=request.user.id)

    try:
        receipt = Receipt.objects.get(receipt_id=receipt_id)
    except Receipt.DoesNotExist:
        receipt = None

    return render(request, 'mobile_pos/checkout.html',{
        'receipt': receipt,
        'store': store,
        'employee': employee,
        'page': 'cart',
    })