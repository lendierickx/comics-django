from django.conf.urls import patterns, include, url
from store_landpage import views


urlpatterns = (
    # Main Aggregate Store
    url(r'^$', views.front_page, name='store_landpage'),
    url(r'landpage$', views.front_page),
    url(r'tos$', views.tos_page, name='store_tos'),
    url(r'privacy$', views.privacy_page, name='store_privacy'),

    # Redirects
#    url(r'^(\d+)/$', views.front_page_redirect),
#    url(r'^(\d+)/(\d+)/$', views.front_page_redirect),
#    url(r'^(\d+)/tos$', views.tos_page_redirect),
#    url(r'^(\d+)/(\d+)/tos$', views.tos_page_redirect),
#    url(r'^(\d+)/privacy$', views.privacy_page_redirect),
#    url(r'^(\d+)/(\d+)/privacy$', views.privacy_page_redirect),
)
