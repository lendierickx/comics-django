from django.conf.urls import patterns, include, url
from . import views


urlpatterns = (
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page, name='robots'),
    url(r'^humans\.txt$', views.humans_txt_page, name='humans'),
    url(r'^F860DA3DF4C3F8A7F5EAFFDA1DB33807\.txt$', views.comodo_txt_page, name='comodo'),
    url(r'^BingSiteAuth\.xml$', views.bing_txt_page, name='bing'),
    url(r'^baidu_verify_ObbdOAW2Jy\.html$', views.baidu_txt_page, name='baidu'),
    url(r'^googled758fc2c6b7f8d7e\.html$', views.google_page, name='google'),

    # Testing that AdminEmailHandler works.
    #url(r'^500$', views.http_500_error_page), # For debugging purposes only!
)
