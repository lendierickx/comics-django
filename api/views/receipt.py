import django_filters
from datetime import datetime
from decimal import *
from django.db.models import Q
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from rest_framework.decorators import detail_route
from ecantina_project import constants
from api.authentication import CsrfExemptSessionAuthentication, BasicAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.receipt import Receipt
from api.serializers import ReceiptSerializer
from django.core.management import call_command

class ReceiptFilter(django_filters.FilterSet):
    has_finished = django_filters.BooleanFilter(name="has_finished")
    class Meta:
        model = Receipt
        fields = ['receipt_id', 'organization', 'store', 'customer', 'has_finished', 'status', 'has_error', 'error', 'has_purchased_online','employee', 'has_shipping',]


class ReceiptViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('email','billing_phone','billing_postal', 'shipping_phone','shipping_postal',)
    filter_class = ReceiptFilter
  
    def get_queryset(self):
        """
            SECURITY: The following query override was set to protect private
            Customer information from being leaked to non-employee staff.
        """
        # If user is an Employee then they have permission to list all the
        # Customers Receipts in our application that belong to the organization,
        # else don't show.
        try:
            customer = Customer.objects.filter(user_id=self.request.user.id)
            employee = Employee.objects.get(user__id=self.request.user.id)
                          
            # Either return all the receipts inside the Organization and/or
            # return all the customers Receipts.
            q = (Q(organization=employee.organization) | Q(customer=customer))
                              
            # Return results.
            return Receipt.objects.filter(q)
        except Customer.DoesNotExist:
            return Receipt.objects.none()
        except Employee.DoesNotExist:
            return Receipt.objects.filter(customer=customer)
        except Receipt.DoesNotExist:
            return Receipt.objects.none() # Worst Case: Return nothing found.

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def apply_discounts(self, request, pk=None):
        """
            Function will iterate through all the products in the cart and
            apply the associated Tag & Promotion discounts per each product.
            Afterwords, each product will have the latest up-to-date price
            associated with the current discounts.
        """
        call_command('receipt_apply_discounts',str(pk))
        return Response({'status': 'success', 'message': '!discounts successfully applied'})

  
    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_tally(self, request, pk=None):
        """
            Function will find the total amount that is owed for the bill and
            save it in the receipt.
        """
        call_command('receipt_tally_up',str(pk))
        return Response({'status': 'success', 'message': 'tallied up totals'})

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_verification(self, request, pk=None):
        """
            Function will verify that the products being checked out are 
            available and can be checked out. If any problems arise this
            function will return a failed message.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        message = self.verify(receipt)
        if message:
            return message
        else:
            return Response({'status': 'success', 'message': 'is ready for checkout'})

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_checkout(self, request, pk=None):
        """
            Function will be used by in-store staff / point of sale device
            to perform transaction handling.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        
        # STEP 1: Verify that our cart can be checked out.
        message = self.verify(receipt)
        if message:
            return message

        # STEP 2: Compute the final bill
        call_command('receipt_tally_up',str(pk))

        # STEP 3: Set our customer information to the receipt if not guest shopper.
        call_command('receipt_checkout',str(pk))
        return Response({'status': 'success', 'message': 'checkout complete'})

    def verify(self, receipt):
        # Verify Receipt.
        if receipt.has_paid:
            return Response({'status': 'failed', 'message': 'customer has already paid for receipt' })
        if receipt.has_finished:
            return Response({'status': 'failed', 'message': 'receipt has already been finsihed' })
        
        # Verify Products.
        for product in receipt.products.all():
            if product.is_sold:
                return Response({'status': 'failed', 'message': 'product was already sold: '+product.name })
            if product.is_listed is False:
                return Response({'status': 'failed', 'message': 'product is no longer sold: '+product.name })

        # Verify Ownership
        if not receipt.has_purchased_online:
            if receipt.employee is None:
                return Response({'status': 'failed', 'message': 'receipts purchased in-store must belong to employee'})

        # Return success
        return None

   
#
# Note: For more information on setting up custom functions, see this url:
# http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
#