import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.authentication import CsrfExemptSessionAuthentication, BasicAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.serializers import TagSerializer
from api.serializers import PrintHistorySerializer
from api.models.ec.print_history import PrintHistory


class PrintHistoryFilter(django_filters.FilterSet):
    filename = django_filters.CharFilter(name="filename", lookup_type=("icontains"))
    class Meta:
        model = PrintHistory
        fields = ['print_id','created','filename','url','organization','store',]


class PrintHistoryViewSet(viewsets.ModelViewSet):
    queryset = PrintHistory.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = PrintHistorySerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly,)
    filter_class = PrintHistoryFilter