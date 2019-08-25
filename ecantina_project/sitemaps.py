from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from api.models.ec.subdomain import SubDomain
from api.models.ec.product import Product


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['store_landpage', 'store_products', 'robots', 'humans', 'comodo', 'store_register', 'store_tos', 'store_privacy', 'authentication',]
    
    def location(self, item):
        return reverse(item)

class SubDomainSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return SubDomain.objects.all()


class ProductsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    
    def items(self):
        return Product.objects.filter(is_sold=False, is_listed=True,)
    
    def lastmod(self, obj):
        return obj.last_updated

# https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/