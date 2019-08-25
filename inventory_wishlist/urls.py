from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/wishlist$', views.wishlist_page),
)
