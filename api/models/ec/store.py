from django.db import models
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.imageupload import ImageUpload
from api.models.ec.employee import Employee
from django.core.cache import caches


class StoreManager(models.Manager):
    """
        Function will lookup and get the single Store entry by the id
        and if nothing was found, it will return a None object.
    """
    def get_or_none(self, store_id):
        try:
            return Store.objects.get(store_id=store_id)
        except Store.DoesNotExist:
            return None


class Store(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('store_id',)
        db_table = 'ec_stores'
    
    # Basic
    objects = StoreManager()
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    description = models.TextField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Variable controls whether the store is no longer listed in our system
    # and Users are not allowed to login/access this store.
    is_suspended = models.BooleanField(default=False, db_index=True)
    
    # Variable controls whether we are to allow displaying and listing
    # this store in our system. Setting to "False" means it won't
    # appear anywhere. This value is read-only and is only adjusted
    # by the staff of eCantina to set it 'False'.
    is_listed = models.BooleanField(default=True, db_index=True)
    
    tax_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.13, # Ontario HST
    )
    
    # Location
    street_name = models.CharField(max_length=63)
    street_number = models.CharField(max_length=31, null=True, blank=True)
    unit_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=63)
    province = models.CharField(
        max_length=63,
        choices=constants.PROVINCE_CHOICES,
    )
    country = models.CharField(
        max_length=63,
        choices=constants.COUNTRY_CHOICES,
    )
    postal = models.CharField(max_length=31)
    currency = models.PositiveSmallIntegerField(
        default=124,
        choices=constants.ISO_4217_CURRENCY_OPTIONS,
    )
    language = models.CharField(
        max_length=2,
        choices=constants.ISO_639_1_LANGUAGE_OPTIONS,
        default='EN',
    )
    
    # Contact
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=10, null=True, blank=True)
    
    # Hours
    is_open_monday = models.BooleanField(default=False)
    is_open_tuesday = models.BooleanField(default=False)
    is_open_wednesday = models.BooleanField(default=False)
    is_open_thursday = models.BooleanField(default=False)
    is_open_friday = models.BooleanField(default=False)
    is_open_saturday = models.BooleanField(default=False)
    is_open_sunday = models.BooleanField(default=False)
    
    monday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_to = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    
    monday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    tuesday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    wednesday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    thursday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    friday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    saturday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)
    sunday_from = models.CharField(choices=constants.STORE_HOUR_OPTIONS, max_length=5, null=True, blank=True)

    # This field controls whether the products in this store will be listed on
    # the main aggregate store.
    is_aggregated = models.BooleanField(default=True, db_index=True)

    # This field controls whether we have a custom shipping rate for the store.
    has_shipping_rate_override = models.BooleanField(default=False, blank=True)

    # The following columns determine if the particular store supports selling
    # the following products and thus granting access to unique user interface.
    is_comics_vendor = models.BooleanField(default=True)
    is_furniture_vendor = models.BooleanField(default=False)
    is_coins_vendor = models.BooleanField(default=False)
    
    # Payment Processing Accounts
    paypal_email = models.EmailField()
    
    # Look and Feel
    header = models.ForeignKey(ImageUpload, null=True, blank=True, related_name='store_header',)
    logo = models.ForeignKey(ImageUpload, null=True, blank=True, related_name='store_logo',)
    style = models.CharField(
        max_length=31,
        choices=constants.TSHOP_THEME_OPTIONS,
        default='ecantina-style-5.css',
    )
    
    # Reference
    organization = models.ForeignKey(Organization, db_index=True)
    employees = models.ManyToManyField(Employee, blank=True)
   
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Store, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            When the sitemaps.xml gets generated for the all the URLS, all
            returned "Organization" objects will have this URL called.
        """
        return "/about/"+str(self.organization.org_id)+"/"+str(self.store_id)
