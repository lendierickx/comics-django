from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.product import Product
from django.core.cache import caches


class ReceiptManager(models.Manager):
    """
        Function will lookup and get the single Receipt entry by the id
        and if nothing was found, it will return a None object.
    """
    def get_or_none(self, receipt_id):
        try:
            return self.get(receipt_id=receipt_id)
        except Receipt.DoesNotExist:
            return None
    
    def get_or_create_for_online_customer(self, customer):
        """
            Function will lookup the Receipt based off the Customer info. If
            a Receipt was not found, then this function will create one and
            return an empty Receipt assigned to this Customer.
        """
        try:
            return self.get(customer=customer,has_finished=False)
        except Receipt.DoesNotExist:
            # Consolidate the address information into a single string.
            billing_address = customer.billing_street_number+' '+customer.billing_street_name
            if customer.billing_unit_number:
                billing_address = customer.billing_unit_number+'-' + billing_address
            shipping_address = customer.shipping_street_number+' '+customer.shipping_street_name
            if customer.shipping_unit_number:
                shipping_address = customer.shipping_unit_number+'-' + shipping_address

            # Create our open receipt.
            return self.create(
                customer=customer,
                email = customer.email,
                billing_address = billing_address,
                billing_phone = customer.billing_phone,
                billing_city = customer.billing_city,
                billing_province = customer.billing_province,
                billing_country = customer.billing_country,
                billing_postal = customer.billing_postal,
                shipping_address = shipping_address,
                shipping_phone = customer.shipping_phone,
                shipping_city = customer.shipping_city,
                shipping_province = customer.shipping_province,
                shipping_country = customer.shipping_country,
                shipping_postal = customer.shipping_postal,
                has_shipping = True,
                has_purchased_online = True,
                payment_method = constants.PAYPAL_PAYMENT_METHOD,
            )


class Receipt(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('last_updated',)
        db_table = 'ec_receipts'
    
    # Meta & Data-Mining
    objects = ReceiptManager()
    organization = models.ForeignKey(Organization, null=True, blank=True, db_index=True)
    store = models.ForeignKey(Store, null=True, blank=True, db_index=True)
    employee = models.ForeignKey(Employee, null=True, blank=True, db_index=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, db_index=True)
    receipt_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)
    purchased = models.DateTimeField(null=True, blank=True, db_index=True)
    
    # Variable holds any instructions / comments the customer would like
    # to attach with his/her purchase.
    comment = models.CharField(max_length=511, null=True, blank=True, default='')
    
    # Variable indicates whether the purchase was made online or in-store.
    has_purchased_online = models.BooleanField(default=False)
    
    # Variable controls HOW the payment was conducted.
    payment_method = models.PositiveSmallIntegerField(
        default=1,
        choices=constants.PAYMENT_METHOD_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(9)],
    )
    
    # Variable controls what is the status of the receipt. This variable is
    # responsible for indicating whether the receipt was started, is ordered,
    # is shipped, etc, etc.
    status = models.PositiveSmallIntegerField(
        default=1,
        choices=constants.STATUS_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        db_index=True
    )
    
    # Variable controls whether the Customer is suppose to pickup the purchase
    # at the store (and have shipping costs wavered) or the Store has to ship
    # out the order to the customer (and apply shipping costs to the total).
    has_shipping = models.BooleanField(default=False, db_index=True)
    
    # Financial
    # Note: Here is the order of computation...
    # sub_total = the total price of all the comics summed
    # sub_total_with_tax = sub_total + tax_amount
    # sub_total_with_tax_and_discount = sub_total_with_tax - discount
    # total_amount = total + shipping costs
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    has_tax = models.BooleanField(default=True)
    tax_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    sub_total_with_tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    shipping_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    has_finished = models.BooleanField(default=False, db_index=True)
    has_paid = models.BooleanField(default=False)
    
    # Payer Information
    email = models.EmailField(null=True, blank=True)
    billing_address = models.CharField(max_length=63, null=True, blank=True)
    billing_phone = models.CharField(max_length=10, null=True, blank=True)
    billing_city = models.CharField(max_length=63, null=True, blank=True)
    billing_province = models.CharField(max_length=63, null=True, blank=True)
    billing_country = models.CharField(max_length=63, null=True, blank=True)
    billing_postal = models.CharField(max_length=31, null=True, blank=True)
    shipping_address = models.CharField(max_length=63, null=True, blank=True)
    shipping_phone = models.CharField(max_length=10, null=True, blank=True)
    shipping_city = models.CharField(max_length=63, null=True, blank=True)
    shipping_province = models.CharField(max_length=63, null=True, blank=True)
    shipping_country = models.CharField(max_length=63, null=True, blank=True)
    shipping_postal = models.CharField(max_length=31, null=True, blank=True)

    # This variable is used to track all the "Products" that are either
    # checked out or are to be purchased (in cart).
    products = models.ManyToManyField(Product, blank=True, related_name='receipt_products')

    # Error handling
    has_error = models.BooleanField(default=False, db_index=True)
    error = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=constants.RECEIPT_ERROR_CHOICES,
        default=0,
    )

    def __str__(self):
        return "Receipt #" + str(self.receipt_id) 

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Receipt, self).save(*args, **kwargs)