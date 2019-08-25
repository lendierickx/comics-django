from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganization
from api.serializers import SectionSerializer
from api.models.ec.section import Section


class SectionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganization, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('organization', 'store',)
