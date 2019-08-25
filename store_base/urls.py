from django.conf.urls import patterns, include, url
from store_base import views


urlpatterns = (
    # HTTP Error URLs.
    url(r'^403$', views.http_403_page, name='403_error'),
    url(r'^404$', views.http_404_page, name='404_error'),

    # Redirection Service URLs.
    url(r'^storefront/([a-z]+)/$', views.storefront_redirect),
    url(r'^storefront/(\d+)/$', views.org_subdomain_redirect),
    url(r'^storefront/(\d+)/(\d+)/$', views.store_subdomain_redirect),
)

# Note:
# http://www.djangobook.com/en/2.0/chapter03.html
