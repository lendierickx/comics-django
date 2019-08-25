import os
import sys
from decimal import *
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
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
    help = 'ETL for computing the totals.'
    
    def add_arguments(self, parser):
        parser.add_argument('receipt_id', nargs='+')
    
    def handle(self, *args, **options):
        #os.system('clear;')  # Clear the console text.
        for receipt_id in options['receipt_id']:
            # Fetch the receipt or quite this function.
            try:
                receipt = Receipt.objects.get(receipt_id=receipt_id)
                self.begin_processing(receipt)
            except Receipt.DoesNotExist:
                pass

    def begin_processing(self, receipt):
        # Iterate through all the products and create a calculate our totals.
        tax_rates = list()
        sub_total_amount = Decimal(0.00)
        total_tax_amount = Decimal(0.00)
        sub_total_amount_with_tax = Decimal(0.00)
        total_discount_amount = Decimal(0.00)
        for product in receipt.products.all():
            # Sub Price
            sub_total_amount += product.sub_price
            
            # Tax
            if product.has_tax:
                tax_rates.append(product.tax_rate)
                total_tax_amount += product.tax_amount
            else:
                tax_rates.append(0)
            
            # Sub Price + Tax
            sub_total_amount_with_tax += product.sub_price_with_tax
            
            # Discounts
            if product.discount > 0:
                if product.discount_type is 1: # Percent
                    rate = Decimal(product.discount) / Decimal(100)
                    discount_amount = Decimal(rate) * Decimal(product.sub_price_with_tax)
                elif product.discount_type is 2: # Amount
                    discount_amount =  product.discount
                total_discount_amount += discount_amount
    
        # Calculate tax
        if len(tax_rates) > 0:
            avg_tax_rate = sum(tax_rates)/len(tax_rates)
            has_tax = avg_tax_rate > 0
        else:
            avg_tax_rate = Decimal(0.00)
            has_tax = False
    
        # Calculate shipping for the specific organization.
        shipping_amount = 0
        if receipt.has_purchased_online:
            if receipt.has_shipping:
                shipping_amount = self.compute_shipping_cost(receipt)

        # Update financials.
        receipt.sub_total = sub_total_amount
        receipt.has_tax = has_tax
        receipt.tax_rate = avg_tax_rate
        receipt.tax_amount = total_tax_amount
        receipt.sub_total_with_tax = sub_total_amount_with_tax
        receipt.discount_amount = total_discount_amount
        receipt.shipping_amount = shipping_amount
        receipt.total_amount = sub_total_amount_with_tax
        receipt.total_amount -= total_discount_amount
        receipt.total_amount += shipping_amount
        receipt.save()

    def compute_shipping_cost(self, receipt):
        if receipt.organization: # CASE 1 of 2: We have a single organization that receipt belongs to.
            return self.compute_shipping_cost_for_organization(receipt.organization)
        else: # CASE 2 of 2: We have no organization.
            return self.compute_shipping_cost_for_aggregate(receipt)

    def compute_shipping_cost_for_organization(self, receipt):
        # Fetch the organization preferences on how to handle shipping rates.
        preference = OrgShippingPreference.objects.get(organization=receipt.organization)
            
        # If the organization set to in-store pickup only, then return zero
        # shipping costs as the cost of travelling to store is handled by
        # customer in real life.
        if preference.is_pickup_only:
            return Decimal(0.00)
    
        # Determine where the receipt is to be shipped
        iso_3166_1_numeric_country_code = 0
        if 'Canada' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 124
        elif 'United States' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 840
        elif 'Mexico' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 484

        # Find the shipping rate to apply for the country and apply it.
        for rate in preference.rates.all():
            if rate.country is iso_3166_1_numeric_country_code:
                # Count how many products we are to ship and apply the
                # appropriate shipping rates. Note: These rates where taken
                # from the following file:
                # - - - - - - - - - - - - - - - - - - - - - - - - -
                # inventory_settings/forms/org_shipping_rates_form
                # - - - - - - - - - - - - - - - - - - - - - - - - -
                comics_count = len(receipt.products.all())
                return rate.get_comics_rate(comics_count)
        
        # Add "Shipping Rate Error" to our cart if cart not found.
        receipt.has_error = True
        receipt.error = constants.SHIPPING_RATE_ERROR_TYPE
        receipt.save()
        print("Org Shipping error for Receipt #"+str(receipt.receipt_id))
        return Decimal(0.00) # Return no rate.

    def compute_shipping_cost_for_aggregate(self, receipt):
        # Determine where the receipt is to be shipped.
        iso_3166_1_numeric_country_code = 0
        if 'Canada' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 124
        elif 'United States' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 840
        elif 'Mexico' in receipt.shipping_country:
            iso_3166_1_numeric_country_code = 484
        
        # Find the rate.
        try:
            rate = UnifiedShippingRate.objects.get(country=iso_3166_1_numeric_country_code)
            comics_count = len(receipt.products.all())
            return rate.get_comics_rate(comics_count)
        except UnifiedShippingRate.DoesNotExist:
            # Add "Shipping Rate Error" to our cart.
            receipt.has_error = True
            receipt.error = constants.SHIPPING_RATE_ERROR_TYPE
            receipt.save()
            print("Unified Shipping error for Receipt #"+str(receipt.receipt_id))
            print("Using country: "+str(iso_3166_1_numeric_country_code))
            print("")
        return Decimal(0.00) # Return no rate.

#
# Note: For more information on setting up custom functions, see this url:
# http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
#