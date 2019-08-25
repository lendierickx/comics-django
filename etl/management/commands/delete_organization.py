import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.section import Section
from api.models.ec.category import Category
from api.models.ec.tag import Tag
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.tag import Tag
from api.models.ec.section import Section


class Command(BaseCommand):
    """
        ----------------------
        delete_organization
        ----------------------
        This command will delete all records associated with a particular organization.
        
        Run in your console:
        $ python manage.py delete_organization {{ ORGANIZATION IDENTIFICATION }}
    """
    help = 'This command will delete all records associated with a particular organization.'
    
    def add_arguments(self, parser):
        parser.add_argument('org_id', nargs='+', type=int)
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for org_id in options['org_id']:
            self.delete_organization(org_id)
        
    def delete_organization(self, org_id):
        # Delete All Receipts
        try:
            for receipt in Receipt.objects.filter(organization_id=org_id):
                print(receipt)
                receipt.delete()
        except Receipt.DoesNotExist:
            pass
        
        # Remove all Products from existing Carts.
        try:
            for receipt in Receipt.objects.filter(products__organization_id=org_id):
                for product in receipt.products.all():
                    receipt.products.remove(product)
        except Receipt.DoesNotExist:
            pass
        except Product.DoesNotExist:
            pass
        
        # Delete All Comics
        try:
            for comic in Comic.objects.filter(organization_id=org_id):
                comic.delete()
        except Comic.DoesNotExist:
            pass

        # Delete All Products
        try:
            for product in Product.objects.filter(organization_id=org_id):
                print(product)
                product.delete()
        except Product.DoesNotExist:
            pass

        # Delete All Promotions
        try:
            for promotion in Promotion.objects.filter(organization_id=org_id):
                promotion.delete()
        except Promotion.DoesNotExist:
            pass

        # Delete All Promotions
        try:
            for tag in Tag.objects.filter(organization_id=org_id):
                tag.delete()
        except Tag.DoesNotExist:
            pass

        # Delete All Promotions
        try:
            for section in Section.objects.filter(organization_id=org_id):
                section.delete()
        except Section.DoesNotExist:
            pass

        # Delete All Employees
        try:
            for employee in Employee.objects.filter(organization_id=org_id):
                employee.delete()
        except Employee.DoesNotExist:
            pass

        # Delete All Store
        try:
            for store in Store.objects.filter(organization_id=org_id):
                store.delete()
        except Store.DoesNotExist:
            pass

        # Delete Organization
        try:
            for org in Organization.objects.filter(org_id=org_id):
                org.delete()
        except Organization.DoesNotExist:
            pass

        print("Deleted All Records Associated with org_id =", org_id)