import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.pulllist import Pulllist
from api.serializers import PulllistSerializer


class PulllistFilter(django_filters.FilterSet):
    series = django_filters.CharFilter(name="series__series_id")
    organization = django_filters.CharFilter(name="organization__org_id")
    store = django_filters.CharFilter(name="store__store_id")
    class Meta:
        model = Pulllist
        fields = ['series','organization', 'store', ]


class PulllistViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Pulllist.objects.all()
    serializer_class = PulllistSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    filter_class = PulllistFilter
    search_fields = ('series__series_sort_name',)
