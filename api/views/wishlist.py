import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.wishlist import Wishlist
from api.serializers import WishlistSerializer


class WishlistFilter(django_filters.FilterSet):
    class Meta:
        model = Wishlist
        fields = ['product', 'customer']


class WishlistViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('product__name',)
    filter_class = WishlistFilter

