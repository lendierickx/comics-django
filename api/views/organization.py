from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOwnerOrReadOnly
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOwnerOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('org_id', 'is_suspended', 'language', 'currency',)

