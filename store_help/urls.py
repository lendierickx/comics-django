from django.conf.urls import patterns, include, url
from store_help import views


urlpatterns = (
    url(r'^help$', views.help_page, name='store_help'),
)
