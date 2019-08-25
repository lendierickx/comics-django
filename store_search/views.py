import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ecantina_project import constants
from inventory_base.forms.imageuploadform import ImageUploadForm
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.models.ec.wishlist import Wishlist


def search_page(request):
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
    
    keyword = request.GET.get('keyword')
    print(keyword);

    # Display the view with all our model information.
    return render(request, 'store_search/view.html',{
        'receipt': receipt,
        'wishlists': wishlists,
        'customer': customer,
        'employee': employee,
        'org': org,
        'store': store,
        'page' : 'search',
        'keyword': keyword,
    })