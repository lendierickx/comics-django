from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import urllib3
from django.views.decorators.cache import cache_page


def robots_txt_page(request):
    return render(request, 'inventory_base/txt/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'inventory_base/txt/humans.txt', {}, content_type="text/plain")


def comodo_txt_page(request):
    return render(request, 'inventory_base/txt/F860DA3DF4C3F8A7F5EAFFDA1DB33807.txt', {}, content_type="text/plain")


def bing_txt_page(request):
    return render(request, 'inventory_base/txt/BingSiteAuth.xml', {}, content_type="text/plain")


def baidu_txt_page(request):
    return render(request, 'inventory_base/txt/baidu_verify_ObbdOAW2Jy.html', {}, content_type="text/plain")


def http_500_error_page(request):
    """
        Simulates generating a HTTP 500 error which will trigger the 'AdminEmailHandler'
        to successfully get called. For debugging purposes only!
    """
    raise Exception('mesg')
    return render(request, 'inventory_base/txt/baidu_verify_ObbdOAW2Jy.html', {}, content_type="text/plain")


def google_page(request):
    return render(request, 'inventory_base/txt/googled758fc2c6b7f8d7e.html', {}, content_type="text/plain")
