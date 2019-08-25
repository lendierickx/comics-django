from django.conf.urls import patterns, include, url
from store_about.views import about


urlpatterns = (
    url(r'^about$', about.about_page),
)
