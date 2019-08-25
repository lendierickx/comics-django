from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/customers$', views.customers_page),
    url(r'^inventory/(\d+)/(\d+)/customer/(\d+)$', views.customer_page),
    url(r'^inventory/(\d+)/(\d+)/customer/(\d+)/profile$', views.profile_page),
    url(r'^inventory/(\d+)/(\d+)/customer/(\d+)/purchases$', views.purchases_page),
    url(r'^inventory/(\d+)/(\d+)/customer/(\d+)/subscriptions$', views.subscriptions_page),
    url(r'^inventory/(\d+)/(\d+)/customer/(\d+)/wishlist$', views.wishlists_page),
)
