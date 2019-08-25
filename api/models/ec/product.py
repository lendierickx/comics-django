import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.imageupload import ImageUpload
from api.models.ec.tag import Tag
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from django.core.cache import caches


class Product(models.Model):
    """
        Model acts as an encompasing object to hold all the different
        type of products in our system such as comics, furniture, etc.
    """
    class Meta:
        app_label = 'api'
        ordering = ('product_id','type')
        db_table = 'ec_products'

    # All products have a unque 'product_id' number which is to be
    # printed on all products in-store or online.
    product_id = models.AutoField(primary_key=True)

    # Every product needs to have a generic name that will show up
    # when customers lookup the product and staff look through the
    # inventory database; furthermore, a product type needs to be
    # specified to tell what sort of product this is.
    name = models.CharField(max_length=511, null=True, blank=True, db_index=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=constants.PRODUCT_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )

    # description that will be displayed to the customer about this product.
    description = models.TextField(default='', blank=True)

    # Date & timekeeping tracking variables.
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # If this product has been purchased by a customer then "True" is set,
    # else "False". Stores are not to display products with 'True' condition.
    # It is important to note that when a product is purchased, the product
    # is not to be deleted from the table, but instead remain in the table
    # and just have the "is_sold" varible to be "True".
    is_sold = models.BooleanField(default=False, db_index=True)

    # This variable controls whether we are allowed to display the product
    # in-store for customers to see or find in the catalog search. Products
    # with this variable set to false are not allowed to show up in search
    # results nor are customers allowed to see this product.
    is_listed = models.BooleanField(default=True, db_index=True)

    # These two variables are used in the store.
    is_new = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)

    # The following variables are to save financial information.
    sub_price = models.DecimalField( # Note: Price before discount applied.
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
    sub_price_with_tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount = models.DecimalField( # Note: Meaured in dollar ($) amount.
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True,
    )
    discount_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=constants.PRODUCT_DISCOUNT_TYPE_OPTIONS,
        default=1,
    )
    price = models.DecimalField( # Note: Price after discount applied.
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    currency = models.PositiveSmallIntegerField(
        default=124,
        choices=constants.ISO_4217_CURRENCY_OPTIONS,
    )
    language = models.CharField(
        max_length=2,
        choices=constants.ISO_639_1_LANGUAGE_OPTIONS,
        default='EN',
    )

    # Every product has images.
    image = models.ForeignKey(ImageUpload, null=True, blank=True,)
    image_url = models.URLField(null=True, blank=True)
    images = models.ManyToManyField(ImageUpload, blank=True, related_name='product_images')

    # Products need to belong to a specific organization and where it is located
    # in the organization (store/section).
    organization = models.ForeignKey(Organization, db_index=True)
    store = models.ForeignKey(Store, db_index=True)
    section = models.ForeignKey(Section, db_index=True)

    # Every product has a list of tags they can belong to. Tags are used
    # to track th
    tags = models.ManyToManyField(Tag, blank=True, related_name='product_tags', db_index=True)

    # Products should have a brand association with it.
    brand = models.ForeignKey(Brand, null=True, blank=True, db_index=True)

    # Every product must belongs to a single cateogry.
    category = models.ForeignKey(Category, db_index=True)

    # The QRCode image with the encoded "product_id" number in it and the boolean
    # to indicate whether the user printed the QR Code to a label or not.
    qrcode = models.ImageField(upload_to='qrcode', null=True, blank=True)
    is_qrcode_printed = models.BooleanField(default=False)

    # Option which forces the online e-commerce system to deny any shipping
    # options for the customer but instead forces the customer to physically
    # go to the store location and pick up the order.
    has_no_shipping = models.BooleanField(default=False)

    # TODO: For future release:
    # Variable controls whether to create a create another product that is a
    # copy of this product when this product gets sold.
    is_unlimited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    # def delete(self, *args, **kwargs):
    #     """
    #         Overrided delete functionality to include deleting the local file
    #         that we have stored on the system. Currently the deletion funciton
    #         is missing this functionality as it's our responsibility to handle
    #         the local files.
    #     """
    #     if self.qrcode:
    #         if os.path.isfile(self.qrcode.path):
    #             os.remove(self.qrcode.path)
    #     super(Product, self).delete(*args, **kwargs) # Call the "real" delete() method

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            When the sitemaps.xml gets generated for the all the URLS, all
            returned "Organization" objects will have this URL called.
        """
        return "/products/"+str(self.product_id)+"/"
