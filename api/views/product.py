from decimal import *
import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import detail_route
from api.pagination import TinyResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly, BelongsToCustomerOrIsEmployeeUser, BelongsToCompanyPolicy
from api.serializers import ProductSerializer
from api.models.ec.product import Product
from api.models.ec.receipt import Receipt
from api.models.ec.comic import Comic
from django.core.management import call_command


class ProductFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(name="brand__name", lookup_type=("icontains"))
    tag = django_filters.CharFilter(name="tag__name", lookup_type=("icontains"))
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    organization = django_filters.CharFilter(name="organization__org_id")
    store = django_filters.CharFilter(name="store__store_id")
    section = django_filters.CharFilter(name="section__section_id")
    category = django_filters.CharFilter(name="category__category_id")
    category_name = django_filters.CharFilter(name="category__name", lookup_type=("icontains"))
    min_sub_price = django_filters.CharFilter(name="sub_price", lookup_type=("gte"))
    max_sub_price = django_filters.CharFilter(name="sub_price", lookup_type=("lte"))
    min_price = django_filters.CharFilter(name="price", lookup_type=("gte"))
    max_price = django_filters.CharFilter(name="price", lookup_type=("lte"))
    min_discount = django_filters.CharFilter(name="discount", lookup_type=("gte"))
    store_aggregated_listing = django_filters.BooleanFilter(name="store__is_aggregated")
    is_org_listed = django_filters.BooleanFilter(name="organization__is_listed")
    is_store_listed = django_filters.BooleanFilter(name="store__is_listed")
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'discount', 'discount_type', 'price', 'cost', 'image', 'organization', 'store', 'section', 'brand', 'brand_name', 'tag', 'is_listed', 'category', 'category_name', 'min_sub_price', 'max_sub_price', 'min_price', 'max_price', 'min_discount', 'is_new', 'is_featured', 'is_qrcode_printed', 'language', 'currency', 'store_aggregated_listing', 'is_org_listed', 'is_store_listed',]


class ProductViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = TinyResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter

    def destroy(self, request, pk=None):
        """
            Override the django-rest "delete" function to include custom
            application logic.
        """
        # Step 1: Get the object
        try:
            product = Product.objects.get(product_id=int(pk))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Step 2: Verify this product is not sold. If it's already sold then
        #         we cannot delete this object.
        if product.is_sold:
            return Response({'status': 'failure', 'message': 'product cannot be deleted because it was already sold.'})
    
        # Step 3: Fetch all the (non-sold) receipts which have this product in
        #         there and remove this product from the Receipt and then
        #         recalculate the Receipt.
        receipts = Receipt.objects.filter(products__product_id=product.product_id,has_finished=False,)
        for receipt in receipts:
            receipt.products.remove(product)
            call_command('receipt_tally_up',str(receipt.receipt_id))
        
        # Step 4: Delete the associated objects and this object.
        try:
            Comic.objects.get(product=product).delete()
        except Exception as e:
            pass
        product.delete()
                
        # STEP 5: Update our Receipt (aka Cart).
        call_command('receipt_tally_up',str(request.receipt.receipt_id))

        # Step 6: Return a response.
        return Response(status=status.HTTP_204_NO_CONTENT)
#
#    @detail_route(methods=['get'], permission_classes=[BelongsToCompanyPolicy])
#    def delete_with_additional_processing(self, request, pk=None):
#        """
#            Removes the product from the inventory permanetly and deletes the associated files.
#            Furthermore if any customer has this product in their cart, the cart gets automatically
#            updated to have totals done
#        """
#        product = self.get_object() # Fetch the product we will be processing.
#        
#        # Fetch all the receipts which have this product in there.
#        receipts = Receipt.objects.filter(products__product_id=product.product_id)
#        for receipt in receipts:
#            receipt.products.remove(receipts)
#            # call_command('myadmincmd')
#            #TODO: Update
#            
#        # Delete the associated comic.
#        try:
#            Comic.objects.get(product=product).delete()
#        except Exception as e:
#            pass
#        
#        # Delete the phyiscal product.
#        product.delete()
#
#        # Return a success message.
#        return Response({'status': 'success', 'message': 'product was deleted from the database and the associated customer receipts have been updated.'})

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def apply_tax_and_discounts(self, request, pk=None):
        """
            Function will add discounts and taxes to the product.
        """
        call_command('product_apply_tax_and_discounts',str(pk))
        return Response({'status': 'success', 'message': 'discounts and taxes successfully applied'})
