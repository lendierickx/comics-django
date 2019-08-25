import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription


@login_required(login_url='/inventory/login')
def pulllist_page(request, org_id, store_id):
    try:
        pulllists = Pulllist.objects.filter(organization_id=org_id)
    except Pulllist.DoesNotExist:
        pulllists = None
    return render(request, 'inventory_pulllist/list/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'pulllists': pulllists,
        'tab':'pulllist',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })

@login_required()
def pulllist_subscriptions_page(request, org_id, store_id, pulllist_id):
    pulllist = Pulllist.objects.get(pulllist_id=pulllist_id)
    try:
        subscriptions = PulllistSubscription.objects.filter(pulllist_id=pulllist_id)
    except PulllistSubscription.DoesNotExist:
        subscriptions = None
    return render(request, 'inventory_pulllist/list/rows.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'pulllist': pulllist,
        'subscriptions': subscriptions,
        'tab':'pulllist',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })

@login_required(login_url='/inventory/login')
def add_pulllist_page(request, org_id, store_id):
    try:
        pulllists = Pulllist.objects.filter(organization_id=org_id)
    except Pulllist.DoesNotExist:
        pulllists = None
    return render(request, 'inventory_pulllist/add/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'pulllists': pulllists,
        'tab':'pulllist',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })

@login_required(login_url='/inventory/login')
def add_pulllist_customer_page(request, org_id, store_id, pulllist_id):
    return render(request, 'inventory_pulllist/customer/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'pulllist': Pulllist.objects.get(pulllist_id=pulllist_id),
        'tab':'pulllist',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })