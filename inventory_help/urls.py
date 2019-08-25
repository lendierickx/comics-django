from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/help$', views.help_page),
)
