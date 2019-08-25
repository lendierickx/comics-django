import json
from datetime import datetime
from django.db.models import Q
from django.db.models import Sum, Count
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product
from api.models.ec.customer import Customer


@login_required(login_url='/inventory/login')
def dashboard_page(request, org_id, store_id):
    today = datetime.now()  # Todays date to be used for this month/year.
    
    #-------------------------------
    # This Months Sales
    #-------------------------------
    monthly_sales = Receipt.objects.filter(
        Q(store_id=store_id) &
        Q(has_paid=True) &
        Q(has_finished=True) &
        Q(purchased__year=today.year) &
        Q(purchased__month=today.month)
    )
    monthly_sales = monthly_sales.order_by('purchased')
    monthly_sales_amount = monthly_sales.aggregate(Sum('total_amount'))
    
    #-------------------------------
    # This Months Orders
    #-------------------------------
    monthly_orders = Receipt.objects.filter(
        Q(store_id=store_id) &
        Q(has_paid=True) &
        Q(has_finished=True) &
        Q(status=1) & # Note: "New Order"
        Q(purchased__year=today.year) &
        Q(purchased__month=today.month)
    )
    monthly_orders = monthly_orders.order_by('purchased')
    monthly_orders_count = monthly_orders.aggregate(Count('pk'))
    
    #-------------------------------
    # This Months New Customers
    #-------------------------------
    organization = Organization.objects.get(org_id=org_id)
    monthly_customers = organization.customers.filter(
        Q(joined__year=today.year) &
        Q(joined__month=today.month)
    )
    monthly_customers = monthly_customers.order_by('joined')
    monthly_customers_count = monthly_customers.aggregate(Count('pk'))
    
    #-------------------------------
    # This Months Pending Orders
    #-------------------------------
    pending_orders = Receipt.objects.filter(
        Q(store_id=store_id) &
        Q(status=1) # Note: "New Order"
    )
    pending_orders = pending_orders.order_by('purchased')
    
    #-------------------------------
    # This years Annual Sales
    #-------------------------------
    annual_sales = Receipt.objects.filter(
        Q(store_id=store_id) &
        Q(has_paid=True) &
        Q(has_finished=True) &
        Q(purchased__year=today.year)
    )
    annual_sales = annual_sales.order_by('purchased')
    
    #-------------------------------
    # Total (On-sale) Inventory
    #-------------------------------
    available_products = Product.objects.filter(
        Q(store_id=store_id) &
        Q(is_sold=False)
    )
    available_products_count = available_products.aggregate(Count('pk'))
    
    return render(request, 'inventory_dashboard/view.html',{
        'today': today,
        'monthly_sales': monthly_sales,
        'monthly_sales_amount': monthly_sales_amount,
        'monthly_orders': monthly_orders,
        'monthly_orders_count': monthly_orders_count,
        'monthly_customers': monthly_customers,
        'monthly_customers_count': monthly_customers_count,
        'pending_orders': pending_orders,
        'annual_sales': annual_sales,
        'available_products_count': available_products_count,
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'tab':'dashboard',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })
