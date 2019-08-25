from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from django.core.cache import caches


DISCOUNT_TYPE_OPTIONS = (
    (1, '%'),
    (2, '$'),
)


class PromotionManager(models.Manager):
    """
        Function will lookup and get the single Organization entry by the id
        and if nothing was found, it will return a None object.
        """
    def get_or_none(self, promotion_id):
        try:
            return self.get(promotion_id=promotion_id)
        except Promotion.DoesNotExist:
            return None


class Promotion(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_promotions'
    
    objects = PromotionManager()
    promotion_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    discount = models.DecimalField( # Note: Meaured in dollar ($) amount.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=DISCOUNT_TYPE_OPTIONS,
        default=1,
    )
    organization = models.ForeignKey(Organization, db_index=True)
    
    def __str__(self):
        return str(self.promotion_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Promotion, self).save(*args, **kwargs)