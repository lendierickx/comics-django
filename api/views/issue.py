import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.models.gcd.issue import GCDIssue
from api.serializers import IssueSerializer
from rest_framework.pagination import PageNumberPagination


class IssueFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="title", lookup_type=("icontains"))
    publisher_name = django_filters.CharFilter(name="publisher_name", lookup_type=("icontains"))
    product_name = django_filters.CharFilter(name="product_name", lookup_type=("icontains"))
    class Meta:
        model = GCDIssue
        fields = ['publisher_name', 'title', 'series', 'issue_id', 'product_name',]


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API endpoint that allows Issues to be viewed or edited.
    """
    queryset = GCDIssue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IssueFilter
