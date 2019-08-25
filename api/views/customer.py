import django_filters
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.serializers import CustomerSerializer
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from itertools import chain

class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(name="first_name", lookup_type=("icontains"))
    last_name = django_filters.CharFilter(name="last_name", lookup_type=("icontains"))
    email = django_filters.CharFilter(name="email", lookup_type=("icontains"))
    phone = django_filters.CharFilter(name="billing_phone", lookup_type=("icontains"))
    postal = django_filters.CharFilter(name="billing_postal", lookup_type=("icontains"))
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'postal', 'is_suspended', 'date_of_birth', 'wants_newsletter', 'wants_flyers',]


class CustomerViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('=customer_id', 'first_name', 'last_name', 'email')
    filter_class = CustomerFilter

    def get_queryset(self):
        """
            SECURITY: The following query override was set to protect private
            Customer information from being leaked to non-employee staff.
        """
        # If user is an Employee then they have permission to list all the
        # customers in our system.
        try:
            Employee.objects.get(user__id=self.request.user.id)
            return Customer.objects.all()
        except Employee.DoesNotExist:
            # Only return the Customer objects that belong to the Customer.
            try:
                return Customer.objects.filter(user_id=self.request.user.id)
            except Customer.DoesNotExist:
                return Customer.objects.none()
