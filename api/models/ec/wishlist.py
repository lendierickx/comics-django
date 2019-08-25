from django.db import models
from api.models.ec.product import Product
from api.models.ec.customer import Customer
from api.models.gcd.issue import GCDIssue
from api.models.gcd.series import GCDSeries
from django.core.cache import caches


class WishlistManager(models.Manager):
    """
        Function will lookup and get the single Wishlist entry by the id
        and if nothing was found, it will return a None object. This function
        is primarly used by the online Store components.
    """
    def filter_by_customer_id_or_none(self, customer_id):
        try:
            return self.filter(
                customer_id=customer_id,
                product__is_sold=False, # DC: Don't show products already sold.
            )
        except Wishlist.DoesNotExist:
            return None


class Wishlist(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'ec_wishlists'
    
    objects = WishlistManager()
    wishlist_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.customer)+" for "+str(self.product)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Wishlist, self).save(*args, **kwargs)