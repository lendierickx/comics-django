import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.serializers import PromotionSerializer
from api.models.ec.helprequest import HelpRequest
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.promotion import Promotion


class PromotionFilter(django_filters.FilterSet):
    class Meta:
        model = Promotion
        fields = ['name',]


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly,)
    filter_class = PromotionFilter
