import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.store import Store
from api.serializers import StoreSerializer

from rest_framework.decorators import detail_route
from api.models.ec.product import Product

class StoreFilter(django_filters.FilterSet):
    store_id = django_filters.CharFilter(name="store__store_id")
    employee = django_filters.CharFilter(name="employees__employee_id")
    organization = django_filters.CharFilter(name="organization__organization_id")
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    description = django_filters.CharFilter(name="description", lookup_type=("icontains"))
    postal = django_filters.CharFilter(name="postal", lookup_type=("icontains"))
    email = django_filters.CharFilter(name="email", lookup_type=("icontains"))
    phone = django_filters.CharFilter(name="phone", lookup_type=("icontains"))
    class Meta:
        model = Store
        fields = ['store_id', 'name', 'description', 'joined', 'last_updated', 'is_suspended','street_name', 'street_number', 'unit_number', 'city', 'province', 'country', 'postal', 'website', 'email', 'phone', 'fax', 'is_open_monday', 'is_open_tuesday', 'is_open_wednesday', 'is_open_thursday', 'is_open_friday', 'is_open_saturday', 'is_open_sunday', 'monday_to', 'tuesday_to', 'wednesday_to', 'thursday_to', 'friday_to', 'saturday_to', 'sunday_to', 'monday_from', 'tuesday_from', 'wednesday_from', 'thursday_from', 'friday_from', 'saturday_from', 'sunday_from', 'organization', 'employees', 'logo', 'tax_rate', 'employee', 'language', 'currency','is_comics_vendor', 'is_furniture_vendor', 'is_coins_vendor', 'is_aggregated',]


class StoreViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = StoreFilter

    @detail_route(methods=['get'], permission_classes=[BelongsToOrganizationOrReadOnly])
    def make_products_pickup_required(self, request, pk=None):
        """
            Function will make all products inside this store to have in-store
            pickup set to True.
        """
        # Fetch the individual store.
        store = self.get_object()
        
        # Fetch all the Products for this store (which are not sold).
        try:
            products = Product.objects.filter(is_sold=False, store=store)
        except Product.DoesNotExist:
            products = None
        
        # Process all products.
        for product in products.all():
            product.has_no_shipping = True
            product.save()

        # Return success message.
        return Response({'status': 'success', 'message': 'All products require in-store pickup now.'})

    @detail_route(methods=['get'], permission_classes=[BelongsToOrganizationOrReadOnly])
    def make_products_pickup_optional(self, request, pk=None):
        """
            Function will make all products inside this store to have in-store
            pickup set to False.
        """
        # Fetch the individual store.
        store = self.get_object()
        
        # Fetch all the Products for this store (which are not sold).
        try:
            products = Product.objects.filter(is_sold=False, store=store)
        except Product.DoesNotExist:
            products = None
        
        # Process all products.
        for product in products.all():
            product.has_no_shipping = False
            product.save()
        
        # Return success message.
        return Response({'status': 'success', 'message': 'All products in store can be ordered only.'})

