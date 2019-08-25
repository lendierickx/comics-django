import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import SubDomainSerializer
from api.models.ec.subdomain import SubDomain


class SubDomainFilter(django_filters.FilterSet):
    class Meta:
        model = SubDomain
        fields = ['name','organization','store',]


class SubDomainViewSet(viewsets.ModelViewSet):
    queryset = SubDomain.objects.all()
    serializer_class = SubDomainSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = SubDomainFilter