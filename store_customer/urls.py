from django.conf.urls import patterns, include, url
from store_customer import views


urlpatterns = (
    url(r'customer/authentication$', views.authentication_page, name="authentication"),

    url(r'customer/my_account$', views.my_account_page),

    url(r'customer/order_history$', views.order_history_page),

    url(r'customer/order_history/(\d+)$', views.order_details_page),

    url(r'customer/wishlist$', views.wishlist_page),

    url(r'customer/my_address$', views.my_address_page),

    url(r'customer/my_billing_address$', views.billing_address_page),

    url(r'customer/my_shipping_address$', views.shipping_address_page),

    url(r'customer/personal_information$', views.personal_info_page),

    url(r'customer/change_password$', views.change_password_page),
)
