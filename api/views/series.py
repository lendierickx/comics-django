import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from api.pagination import RegularResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.models.gcd.series import GCDSeries
from api.serializers import SeriesSerializer


class SeriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    publisher_name = django_filters.CharFilter(name="publisher__name", lookup_type=("icontains"))
    min_year_began = django_filters.NumberFilter(name="year_began", lookup_type='gte')
    max_year_ended = django_filters.NumberFilter(name="year_ended", lookup_type='lte')
    class Meta:
        model = GCDSeries
        fields = ['name', 'publisher_name', 'min_year_began', 'max_year_ended', 'language', 'country', 'year_ended_uncertain', 'year_ended',]


class SeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = GCDSeries.objects.all()
    serializer_class = SeriesSerializer
    pagination_class = RegularResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SeriesFilter
