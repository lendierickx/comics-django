import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inventory_base.forms.loginform import LoginForm
from api.models.ec.employee import Employee
from api.models.ec.store import Store


def login_page(request):
    # If the user is already authenticated then simply redirect to the latest
    # dashboard page, else load the login page.
    if request.user.is_authenticated():
        employee = Employee.objects.get(user__id=request.user.id)
        store = Store.objects.filter(organization=employee.organization)[0]
        dashboard_url = "/inventory/"+str(employee.organization_id)
        dashboard_url += "/"+str(store.store_id)+"/"+"dashboard"
        return HttpResponseRedirect(dashboard_url)
    else:
        return render(request, 'inventory_login/view.html',{
            'form': LoginForm(),
        })