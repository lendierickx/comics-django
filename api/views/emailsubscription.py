import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import AnonymousWriteAndIsEmployeeRead
from api.models.ec.emailsubscription import EmailSubscription
from api.serializers import EmailSubscriptionSerializer


class EmailSubscriptionFilter(django_filters.FilterSet):
    class Meta:
        model = EmailSubscription
        fields = ['store','organization', ]


class EmailSubscriptionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = EmailSubscription.objects.all()
    serializer_class = EmailSubscriptionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (AnonymousWriteAndIsEmployeeRead,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EmailSubscriptionFilter

