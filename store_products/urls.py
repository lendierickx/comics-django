from django.conf.urls import patterns, include, url
from store_products.views import product_list
from store_products.views import product_details


urlpatterns = (
    # Product Listing
    #----------------------
    url(r'^products/grid$', product_list.list_page, name='store_products'),

    # Product Details
    #----------------------
    url(r'^products/(\d+)/$', product_details.details_page),
)
