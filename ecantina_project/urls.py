"""ecantina_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static, settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from .sitemaps import SubDomainSitemap
from .sitemaps import ProductsSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'subdomains': SubDomainSitemap,
    'products': ProductsSitemap,
}


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),  # Authentication
    url(r'^admin/', include(admin.site.urls)), # Administration
    url(r'', include('store_base.urls')),
    url(r'', include('store_landpage.urls')),
    url(r'', include('store_about.urls')),
    url(r'', include('store_products.urls')),
    url(r'', include('store_blog.urls')),
    url(r'', include('store_checkout.urls')),
    url(r'', include('store_customer.urls')),
    url(r'', include('store_register.urls')),
    url(r'', include('store_help.urls')),
    url(r'', include('store_search.urls')),
    url(r'', include('mobile_pos.urls')),
    url(r'', include('inventory_base.urls')),
    url(r'', include('inventory_catalog.urls')),
    url(r'', include('inventory_login.urls')),
    url(r'', include('inventory_checkout.urls')),
    url(r'', include('inventory_order.urls')),
    url(r'', include('inventory_customer.urls')),
    url(r'', include('inventory_dashboard.urls')),
    url(r'', include('inventory_help.urls')),
    url(r'', include('inventory_print_label.urls')),
    url(r'', include('inventory_products.urls')),
    url(r'', include('inventory_setting.urls')),
    url(r'', include('inventory_email.urls')),
    url(r'', include('inventory_pulllist.urls')),
    url(r'', include('inventory_register.urls')),
    url(r'', include('inventory_wishlist.urls')),
    url(r'', include('api.urls')),

    # PayPal
    url(r'^checkout/paypal/', include('paypal.standard.ipn.urls')),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Custom errors.
handler404 = "store_base.views.http_404_page"
