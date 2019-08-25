import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsEmployeeUser
from api.serializers import ImageBinaryUploadSerializer
from api.models.ec.helprequest import HelpRequest
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.imagebinaryupload import ImageBinaryUpload


class ImageBinaryUploadFilter(django_filters.FilterSet):
    class Meta:
        model = ImageBinaryUpload
        fields = ['owner_id',]


class ImageBinaryUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageBinaryUpload.objects.all()
    serializer_class = ImageBinaryUploadSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = ImageBinaryUploadFilter
