import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.wishlist import Wishlist


@login_required(login_url='/inventory/login')
def wishlist_page(request, org_id, store_id):
    # Fetch all the pullists belonging to the current organization.
    try:
        wishlists = Wishlist.objects.filter(
            product__organization_id=org_id
        )
    except Wishlist.DoesNotExist:
        wishlists = None
    
    # Render View
    return render(request, 'inventory_wishlist/view.html',{
        'wishlists': wishlists,
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'tab':'wishlist',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })
