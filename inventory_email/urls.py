from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/email/add_article$', views.add_article_page),
)
