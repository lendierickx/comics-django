from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from django.core.cache import caches


class CustomerManager(models.Manager):
    def get_or_create_for_user_email(self, user_email):
        """
            Function will lookup the customer based off the user's email. If
            a customer was not found, then this function will create one and
            return an empty customer assigned to this user.
        """
        # Find the User.
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return None
        
        # Either fetch existing Customer or create it.
        try:
            customer = self.get(email=user_email)
            
            # Defensive Code: If missing 'user', then update it.
            if customer.user is None:
                customer.user = user
                customer.save()
            
            return customer
        except Customer.DoesNotExist:
            return self.create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )


class Customer(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('last_name','first_name')
        db_table = 'ec_customers'
    
    # System
    objects = CustomerManager()
    customer_id = models.AutoField(primary_key=True)
    joined = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False)
    is_tos_signed = models.BooleanField(default=False)
    wants_newsletter = models.BooleanField(default=False)
    wants_flyers = models.BooleanField(default=False)
    
    # Email Verification
    is_verified = models.BooleanField(default=False)
    verification_key = models.CharField(max_length=63, default='', blank=True)
    
    # Name & Contact
    first_name = models.CharField(max_length=63, db_index=True)
    last_name = models.CharField(max_length=63, db_index=True)
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    
    # Date of Birth
    date_of_birth = models.DateField(default=datetime.now)
    
    # Billing Info
    billing_phone = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    billing_street_name = models.CharField(max_length=63)
    billing_street_number = models.CharField(max_length=15)
    billing_unit_number = models.CharField(max_length=15, null=True, blank=True)
    billing_city = models.CharField(max_length=63)
    billing_province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    billing_country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    billing_postal = models.CharField(max_length=31, db_index=True)
    
    # Shipping Info
    is_shipping_same_as_billing = models.BooleanField(default=False)
    shipping_phone = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    shipping_street_name = models.CharField(max_length=63)
    shipping_street_number = models.CharField(max_length=15)
    shipping_unit_number = models.CharField(max_length=15, null=True, blank=True)
    shipping_city = models.CharField(max_length=63)
    shipping_province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    shipping_country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    shipping_postal = models.CharField(max_length=31, db_index=True)
    
    # Legal
    has_consented = models.BooleanField(default=False)
    
    # References.
    user = models.ForeignKey(User, null=True, blank=True)
    profile = models.ForeignKey(ImageUpload, null=True, blank=True)
    qrcode = models.ImageField(upload_to='qrcode', null=True, blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Customer, self).save(*args, **kwargs)
