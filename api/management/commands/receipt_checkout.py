import os
import sys
from datetime import datetime
from decimal import *
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.tag import Tag
from api.models.ec.product import Product
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.unified_shipping_rates import UnifiedShippingRate


class Command(BaseCommand):
    help = 'ETL for checking out receipts.'
    
    def add_arguments(self, parser):
        parser.add_argument('receipt_id', nargs='+')
    
    def handle(self, *args, **options):
        for receipt_id in options['receipt_id']:
            try:
                receipt = Receipt.objects.get(receipt_id=receipt_id)
                self.begin_processing(receipt)
            except Receipt.DoesNotExist:
                pass

    def begin_processing(self, receipt):
        # STEP 1: Handle Customer.
        if receipt.customer:
            billing_address = receipt.customer.billing_street_number
            billing_address += ' ' + receipt.customer.billing_street_name
            if receipt.customer.billing_unit_number:
                billing_address = receipt.customer.billing_unit_number + '-' + billing_address

            shipping_address = receipt.customer.shipping_street_number
            shipping_address += ' ' + receipt.customer.shipping_street_name
            if receipt.customer.shipping_unit_number:
                shipping_address = receipt.customer.shipping_unit_number + '-' + shipping_address

            receipt.email = receipt.customer.email
            receipt.billing_address = billing_address
            receipt.billing_phone = receipt.customer.billing_phone
            receipt.billing_city = receipt.customer.billing_city
            receipt.billing_province = receipt.customer.billing_province
            receipt.billing_country = receipt.customer.billing_country
            receipt.billing_postal = receipt.customer.billing_postal
            receipt.shipping_address = shipping_address
            receipt.shipping_phone = receipt.customer.shipping_phone
            receipt.shipping_city = receipt.customer.shipping_city
            receipt.shipping_province = receipt.customer.shipping_province
            receipt.shipping_country = receipt.customer.shipping_country
            receipt.shipping_postal = receipt.customer.shipping_postal

        # STEP 2: Finalize our receipt.
        receipt.purchased = datetime.today()
        receipt.has_finished = True
        receipt.has_paid = True
        receipt.status = constants.IN_STORE_SALE_STATUS
        receipt.payment_method = constants.CASH_PAYMENT_METHOD
        receipt.save()
        
        # STEP 3: Inform our products that they are sold out.
        for product in receipt.products.all():
            product.is_sold = True
            product.save()