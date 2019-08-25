from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from django.core.cache import caches


class HelpRequest(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('submission_date',)
        db_table = 'ec_help_requests'
    
    help_id = models.AutoField(primary_key=True)
    subject = models.PositiveSmallIntegerField(
        default=1,
        choices=constants.HELP_REQUEST_SUBJECT_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    subject_url = models.URLField(null=True, blank=True)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    
    # References
    screenshot = models.ForeignKey(ImageUpload, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, blank=True)
    store = models.ForeignKey(Store, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)

    def __str__(self):
        return "Ticket #" + str(self.help_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(HelpRequest, self).save(*args, **kwargs)