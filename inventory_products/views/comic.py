import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models.gcd.issue import GCDIssue
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.brand import Brand
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.category import Category
from api.models.ec.tag import Tag
from inventory_products.forms import IssueForm
from inventory_products.forms import ComicForm
from inventory_products.forms import ImageUploadForm
from inventory_products.forms import ProductForm


def lazy_load_brand(issue):
    """
        Find the brand based on the publisher name and return it, else
        create a new brand based on the publisher name and return it.
    """
    # Load or create the brand.
    try:
        brand = Brand.objects.get(name=issue.series.publisher.name)
    except Exception as e:
        brand = Brand.objects.create(
            name = issue.series.publisher.name,
        )
    return brand

@login_required(login_url='/inventory/login')
def comic_page(request, org_id, store_id, issue_id, product_id):
    org = Organization.objects.get(org_id=org_id)
    employee = Employee.objects.get(user__id=request.user.id)
    store = Store.objects.get(store_id=store_id)
    stores = Store.objects.filter(organization=org, is_suspended=False)
    try:
        sections = Section.objects.filter(store=store)
    except Section.DoesNotExist:
        sections = None

    try:
        issue = GCDIssue.objects.get(issue_id=issue_id)
    except GCDIssue.DoesNotExist:
        issue = None

    try:
        tags = Tag.objects.filter(organization=org)
    except Tag.DoesNotExist:
        tags = None

    try:
        comic = Comic.objects.get(product_id=product_id)
        comic_form = ComicForm(instance=comic)
        product_form = ProductForm(instance=comic.product)
    except Comic.DoesNotExist:
        comic_form = ComicForm()
        product_form = ProductForm(initial={'price': 5.00,'name':str(issue),'is_new': True,})

    if stores is not None:
        # http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
        product_form.fields["store"].queryset = stores
    if sections is not None:
        product_form.fields["section"].queryset = sections

    # Render page
    return render(request, 'inventory_products/comic/modify/view.html',{
        'org': org,
        'store': store,
        'issue': issue,
        'tab':'add',
        'product_form': product_form,
        'comic_form': comic_form,
        'issue': issue,
        'brand': lazy_load_brand(issue),
        'tags': tags,
        'employee': Employee.objects.get(user__id=request.user.id),
        'locations': Store.objects.filter(organization_id=org_id),
    })