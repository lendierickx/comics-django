from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    url(r'^inventory/register/step1$', views.step1_page),
    url(r'^inventory/register/step2$', views.step2_page),
    url(r'^inventory/register/step3$', views.step3_page),
    url(r'^inventory/register/step4$', views.step4_page),
    url(r'^inventory/register/step5$', views.step5_page),
)
