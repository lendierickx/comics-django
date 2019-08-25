from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/catalog$', views.catalog_page),
    url(r'^inventory/(\d+)/(\d+)/catalog/add_comic$', views.catalog_add_page),
    url(r'^inventory/(\d+)/(\d+)/catalog/(\d+)$', views.catalog_edit_page),
)
