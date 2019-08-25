from django.conf.urls import patterns, include, url
from inventory_print_label.views import comic, print_history, print_redo


urlpatterns = (
    url(r'^inventory/(\d+)/(\d+)/print_labels/comics$', comic.comics_print_labels_page),
    url(r'^inventory/(\d+)/(\d+)/print_labels/comics/series/(\d+)$', comic.series_qrcodes_page),
    url(r'^inventory/(\d+)/(\d+)/print_labels/comics/all$', comic.all_qrcodes_page),
    url(r'^inventory/(\d+)/(\d+)/print_history$', print_history.print_history_page),
    url(r'^inventory/(\d+)/(\d+)/print_redo$', print_redo.comics_redo_page),
)
