from django.db import models
from django.contrib.auth.models import User
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from api.models.ec.customer import Customer
from django.core.cache import caches


class OrganizationManager(models.Manager):
    """
        Function will lookup and get the single Organization entry by the id
        and if nothing was found, it will return a None object.
    """
    def get_or_none(self, org_id):
        try:
            return self.get(org_id=org_id)
        except Organization.DoesNotExist:
            return None


class Organization(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_organizations'
    
    # Basic
    objects = OrganizationManager()
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    description = models.TextField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Variable controls whether the Organization is no longer listed in our
    # system and Users are not allowed to login/access it.
    is_suspended = models.BooleanField(default=False, db_index=True)
    
    # Variable controls whether we are to allow displaying and listing
    # this Organization in our system. Setting to "False" means it won't
    # appear anywhere. This value is read-only and is only adjusted
    # by the staff of eCantina to set it 'False'.
    is_listed = models.BooleanField(default=True, db_index=True)
    
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
    
    # Social Media
    twitter = models.CharField(max_length=15, null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    google_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    flickr_url = models.URLField(null=True, blank=True)

    # Payment Processing Accounts
    paypal_email = models.EmailField()

    # Look and Feel
    header = models.ForeignKey(ImageUpload, null=True, blank=True, related_name='org_header',)
    logo = models.ForeignKey(ImageUpload, null=True, blank=True, related_name='org_logo',)
    style = models.CharField(
        max_length=31,
        choices=constants.TSHOP_THEME_OPTIONS,
        default='ecantina-style-5.css',
    )

    # Users
    administrator = models.ForeignKey(User, null=True,)
    customers = models.ManyToManyField(Customer, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
        super(Organization, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            When the sitemaps.xml gets generated for the all the URLS, all
            returned "Organization" objects will have this URL called.
        """
        return "/about/"+str(self.org_id)
