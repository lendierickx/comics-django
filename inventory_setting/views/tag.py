import json
from datetime import datetime
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.models.ec.section import Section
from api.models.ec.tag import Tag


@login_required(login_url='/inventory/login')
def tags_settings_page(request, org_id, store_id):
    return render(request, 'inventory_setting/tag/view.html',{
        'org': Organization.objects.get(org_id=org_id),
        'store': Store.objects.get(store_id=store_id),
        'employee': Employee.objects.get(user__id=request.user.id),
        'tab':'tags_settings',
        'locations': Store.objects.filter(organization_id=org_id),
    })