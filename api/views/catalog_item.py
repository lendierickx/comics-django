import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganization
from api.serializers import CatalogItemSerializer
from api.models.ec.catalog_item import CatalogItem


class CatalogItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    class Meta:
        model = CatalogItem
        fields = ['name',]


class CatalogItemViewSet(viewsets.ModelViewSet):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganization, IsAuthenticated,)
    filter_class = CatalogItemFilter