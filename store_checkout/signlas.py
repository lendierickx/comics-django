from datetime import datetime
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from ecantina_project import constants
from api.models.ec.receipt import Receipt
from api.models.ec.product import Product


def paypal_checkout_online_receipt(receipt):
    # STEP 1: Set our customer information to the receipt if not guest shopper.
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
    receipt.status = constants.ONLINE_SALE_STATUS
    receipt.payment_method = constants.PAYPAL_PAYMENT_METHOD
    receipt.save()
        
    # STEP 3: Inform our products that they are sold out.
    for product in receipt.products.all():
        product.is_sold = True
        product.save()


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print("Begin PayPal Processing")
    
    # If PayPal returns an indication that our payment was successful and
    # the custom callback function matches 'perform_receipt_checkout' then
    # find the Customer's Receipt and set it to succesffully checked out!
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print(ipn_obj)
        #if ipn_obj.custom == "perform_receipt_checkout":
        receipt_id = int(ipn_obj.invoice)
        try:
            receipt = Receipt.objects.get(receipt_id=receipt_id)
            print(receipt)
            paypal_checkout_online_receipt(receipt)
        except Receipt.DoesNotExist:
            print("Cannot find Receipt", str(receipt_id))
    else:
        print("PayPal Error", str(ipn_obj.payment_status))


# IMPORTANT: When PayPal sends a transaction notification to our server
#            our "django-paypal" library will handle accepting it and
#            then invoking the following function called "payment_signal".
valid_ipn_received.connect(show_me_the_money)

# Note:
# Documents: https://django-paypal.readthedocs.org/en/stable/standard/ipn.html