from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches
from django.contrib.sites.models import Site

class SubDomain(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_subdomains'
    
    sub_domain_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True, unique=True, null=True, blank=True,)
    organization = models.ForeignKey(Organization, null=True, blank=True, db_index=True)
    store = models.ForeignKey(Store, null=True, blank=True, db_index=True)

    def __str__(self):
        if self.name is None:
           return str(self.sub_domain_id)
        else:
            return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(SubDomain, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            When the sitemaps.xml gets generated for the all the URLS, all
            returned "Subdomain" objects will have this URL called.
        """
        return "/storefront/"+str(self.name)+"/"

