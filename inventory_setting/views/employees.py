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
from inventory_setting.forms.storeform import StoreForm
from inventory_setting.forms.organizationform import OrganizationForm
from inventory_setting.forms.userform import UserForm
from inventory_setting.forms.sectionform import SectionForm
from inventory_setting.forms.employeeform import EmployeeForm


# Listing
#----------------


@login_required(login_url='/inventory/login')
def users_list_settings_page(request, org_id, store_id, this_store_id):
    organization = Organization.objects.get(org_id=org_id)
    
    # Try to find the store we will be processing and their respected employees.
    try:
        this_store = Store.objects.get(store_id=this_store_id)
        employees = this_store.employees.all()
    except Store.DoesNotExist:
        this_store = None
        employees = Employee.objects.filter(organization=organization)

    return render(request, 'inventory_setting/employee/list/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'this_store': this_store,
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user__id=request.user.id),
        'employees': employees,
        'form': StoreForm(),
        'tab':'users_settings',
        'locations': Store.objects.filter(organization_id=org_id),
        'src_urls': ['inventory_setting/employee/list/suspend_modal.html'],
    })


# Add
#----------------


@login_required(login_url='/inventory/login')
def add_employee_page(request, org_id, store_id):
    organization = Organization.objects.get(org_id=org_id)
    return render(request, 'inventory_setting/employee/add/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user__id=request.user.id),
        'employee_form': EmployeeForm(initial={'joined':datetime.now()}),
        'user_form': UserForm(),
        'tab':'users_settings',
        'locations': Store.objects.filter(organization_id=org_id),
    })



# Edit
#----------------


@login_required(login_url='/inventory/login')
def edit_user_settings_page(request, org_id, store_id, this_employee_id):
    # Try to find the user.
    try:
        this_employee = Employee.objects.get(employee_id=this_employee_id)
    except Employee.DoesNotExist:
        this_employee = None
    
    organization = Organization.objects.get(org_id=org_id)
    return render(request, 'inventory_setting/employee/edit/view.html',{
        'org': organization,
        'store': Store.objects.get(store_id=store_id),
        'stores': Store.objects.filter(organization=organization),
        'employee': Employee.objects.get(user__id=request.user.id),
        'this_employee': this_employee,
        'form': EmployeeForm(instance=this_employee),
        'user_form': UserForm() if this_employee is None else UserForm(instance=this_employee.user),
        'tab':'users_settings',
        'locations': Store.objects.filter(organization_id=org_id),
    })


# User - Common
#----------------


@login_required()
def ajax_assign_employee_to_store(request, org_id, store_id):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            this_employee_id = request.POST['this_employee_id']
            this_store_id = request.POST['this_store_id']
            
            # Find store & employee
            try:
                store = Store.objects.get(store_id=this_store_id)
            except Store.DoesNotExist:
                store = None
            try:
                employee = Employee.objects.get(employee_id=this_employee_id)
            except Employee.DoesNotExist:
                employee = None
        
            if employee is not None and store is not None:
                # Assignment - If employee exists for this store then remove it,
                # else then add it in there.
                if employee in store.employees.all():
                    store.employees.remove(employee)
                else:
                    store.employees.add(employee)
                response_data = {'status': 'success', 'message': 'saved',}
            else:
                response_data = {'status': 'failed', 'message': 'missing objects',}
    return HttpResponse(json.dumps(response_data), content_type="application/json")