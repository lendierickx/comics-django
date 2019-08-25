import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee


def about_page(request):
    employee = Employee.objects.get_for_user_id_or_none(request.user.id)
    organization = request.organization
    store = request.store

    # Redirect the user to a forbidden error if the store or organization
    # are not listed.
    if organization:
        if organization.is_listed is False:
            return HttpResponseRedirect("/403")
    if store:
        if store.is_listed is False:
            return HttpResponseRedirect("/403")

    # Fetch either all the stores within the organization or fetch the
    # individual store at the 'store_id' value.
    stores = None
    if store:
        stores = Store.objects.filter(store_id=store.store_id)
    else:
        stores = Store.objects.filter(organization=organization)

    return render(request, 'store_about/about.html',{
        'page_metadata': 'store_landpage/meta.html',
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'org' : organization,
        'store': store,
        'stores' : stores,
        'page' : 'about',
    })
