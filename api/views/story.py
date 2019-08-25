import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import StorySerializer
from api.models.gcd.story import GCDStory


class StoryFilter(django_filters.FilterSet):
    class Meta:
        model = GCDStory
        fields = ['issue',]


class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = GCDStory.objects.all()
    serializer_class = StorySerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = StoryFilter