import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.serializers import TagSerializer
from api.models.ec.tag import Tag
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.promotion import Promotion


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ['name',]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly,)
    filter_class = TagFilter