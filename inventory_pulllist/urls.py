from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/pulllist$', views.pulllist_page),
    url(r'^inventory/(\d+)/(\d+)/pulllist/(\d+)/subscriptions$', views.pulllist_subscriptions_page),
    url(r'^inventory/(\d+)/(\d+)/pulllist/add_pulllist$', views.add_pulllist_page),
    url(r'^inventory/(\d+)/(\d+)/pulllist/(\d+)/add_customer$', views.add_pulllist_customer_page),
)
