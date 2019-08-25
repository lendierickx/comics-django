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
from api.models.ec.helprequest import HelpRequest
from inventory_help.forms import HelpRequestForm


@login_required(login_url='/inventory/login')
def help_page(request, org_id, store_id):
    return render(request, 'inventory_help/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'form': HelpRequestForm(),
        'tab':'help',
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
        'src_urls': ['inventory_help/success_modal.html'],
    })