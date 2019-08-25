import os
import sys
from decimal import *
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from api.models.ec.organization import Organization
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.tag import Tag
from api.models.ec.product import Product


class Command(BaseCommand):
    help = 'ETL will add discounts and taxes to the product.'
    
    def add_arguments(self, parser):
        parser.add_argument('product_id', nargs='+')
    
    def handle(self, *args, **options):
        #os.system('clear;')  # Clear the console text.
        for product_id in options['product_id']:
            # Fetch the receipt or quite this function.
            try:
                product = Product.objects.get(product_id=product_id)
                self.begin_processing(product)
            except Product.DoesNotExist:
                pass

    def begin_processing(self, product):
        try:
            promotions = Promotion.objects.filter(organization=product.organization)
        except Promotion.DoesNotExist:
            Promotions = None

        if product.store.tax_rate > 0:
            product.tax_rate = product.store.tax_rate
            product.tax_amount = product.sub_price * product.tax_rate
            product.sub_price_with_tax = product.tax_amount + product.sub_price
            
        # Iterate through all the Tags and sum their discounts
        total_percent = Decimal(0.00)
        total_amount = Decimal(0.00)
        for tag in product.tags.all():
            if tag.discount_type is 1:
                total_percent += tag.discount
            if tag.discount_type is 2:
                total_amount += tag.discount
        
        # Iterate through all the Promotions and sum their discounts.
        for promotion in promotions:
            if promotion.discount_type is 1:
                total_percent += promotion.discount
            if promotion.discount_type is 2:
                total_amount += promotion.discount
            
        # Compute the discount
        if total_percent > 0:
            product.discount = product.sub_price_with_tax * (total_percent/100)
                    
            if total_amount > 0:
                product.discount += total_amount
                    
            if total_percent > 0 or total_amount > 0:
                product.discount_type = 2
                
        # Compute final price.
        product.price = (product.sub_price_with_tax - product.discount)
        product.save()
