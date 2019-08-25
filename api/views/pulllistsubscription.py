import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.serializers import PulllistSubscriptionSerializer


class PulllistSubscriptionFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(name="customer__customer_id")
    organization = django_filters.CharFilter(name="organization__org_id")
    pulllist = django_filters.CharFilter(name="pulllist__pulllist_id")
    class Meta:
        model = PulllistSubscription
        fields = ['customer','organization', 'pulllist', ]


class PulllistSubscriptionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = PulllistSubscription.objects.all()
    serializer_class = PulllistSubscriptionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PulllistSubscriptionFilter

