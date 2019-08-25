from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    # Dashboard
    #----------------------
    url(r'^inventory/(\d+)/(\d+)$', views.dashboard_page),
    url(r'^inventory/(\d+)/(\d+)/dashboard$', views.dashboard_page),
)
