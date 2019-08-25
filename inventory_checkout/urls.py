from django.conf.urls import patterns, include, url
from inventory_checkout.views import pos_session
from inventory_checkout.views import pos_customer
from inventory_checkout.views import pos_item
from inventory_checkout.views import pos_receipt
from inventory_checkout.views import pos_record


urlpatterns = (
    # Session
    #-----------
    url(r'^inventory/(\d+)/(\d+)/checkout$', pos_session.checkout_page),

    # Customers
    #-----------
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/customer$', pos_customer.checkout_page),

    # Items
    #-----------
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items$', pos_item.checkout_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/content$', pos_item.content_page),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/(\d+)/change_discount_type$', pos_item.ajax_change_discount_type),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/(\d+)/change_discount_amount$', pos_item.ajax_change_discount_amount),
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/change_tax$', pos_item.ajax_change_tax),

    # Receipt
    #-----------
    url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/receipt$', pos_receipt.checkout_page),

    # Record
    #-----------
    url(r'^inventory/(\d+)/(\d+)/checkout_record$', pos_record.pos_record_page),
)
