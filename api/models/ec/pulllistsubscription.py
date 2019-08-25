from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.pulllist import Pulllist
from django.core.cache import caches


class PulllistSubscription(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'ec_pulllists_subscriptions'
    
    subscription_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    pulllist = models.ForeignKey(Pulllist, db_index=True)
    customer = models.ForeignKey(Customer, db_index=True)
    copies = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.subscription_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(PulllistSubscription, self).save(*args, **kwargs)