from django.conf.urls import patterns, include, url
from store_register import views


urlpatterns = (
    url(r'^store/register/step1$', views.registration_step1_page, name='store_register'),
    url(r'^store/register/step2$', views.registration_step2_page),
    url(r'^store/register/step3$', views.registration_step3_page),
    url(r'^store/register/step4$', views.registration_step4_page),
    url(r'^store/register/step5$', views.registration_step5_page),
)
