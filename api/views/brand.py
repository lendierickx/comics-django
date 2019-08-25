import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import TagSerializer
from api.serializers import BrandSerializer
from api.models.ec.brand import Brand
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.promotion import Promotion


class BrandFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    class Meta:
        model = Brand
        fields = ['brand_id', 'name',]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = BrandFilter