from django.db import models
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches


class EmailSubscription(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('submission_date',)
        db_table = 'ec_email_subscriptions'
    
    subscription_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    # References
    store = models.ForeignKey(Store, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)

    def __str__(self):
        return "Subscription #" + str(self.subscription_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(EmailSubscription, self).save(*args, **kwargs)