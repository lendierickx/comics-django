from django.conf.urls import patterns, include, url
from mobile_pos import views


urlpatterns = (
    url(r'^mobile/pos/login$', views.login_page),
    url(r'^mobile/pos/pick_store$', views.pick_store_page),
    url(r'^mobile/pos/(\d+)/dashboard$', views.dashboard_page),
    url(r'^mobile/pos/(\d+)/remove_product$', views.remove_product_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/$', views.cart_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/product_scanner$', views.scanner_page),
    url(r'^mobile/pos/(\d+)/cart/(\d+)/checkout$', views.checkout_page),
)
