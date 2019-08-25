from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models.ec.imagebinaryupload import ImageBinaryUpload
from api.models.ec.customer import Customer
from api.models.ec.store import Store
from api.models.ec.organization import Organization
from api.models.ec.product import Product
from api.models.ec.employee import Employee
from api.models.ec.comic import Comic
from api.models.ec.receipt import Receipt
from api.models.ec.helprequest import HelpRequest
from api.models.ec.imageupload import ImageUpload
from api.models.ec.promotion import Promotion
from api.models.ec.section import Section
from api.models.ec.wishlist import Wishlist
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.models.ec.tag import Tag
from api.models.ec.brand import Brand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.story import GCDStory
from api.models.ec.category import Category
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from api.models.ec.emailsubscription import EmailSubscription
from api.models.ec.unified_shipping_rates import UnifiedShippingRate
from api.models.ec.print_history import PrintHistory
from api.models.ec.subdomain import SubDomain
from api.models.ec.banned_domain import BannedDomain
from api.models.ec.banned_ip import BannedIP
from api.models.ec.banned_word import BannedWord
from api.models.ec.catalog_item import CatalogItem


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100,style={'placeholder': 'Email'})
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'joined', 'last_updated', 'is_suspended', 'first_name', 'last_name', 'email', 'billing_phone', 'billing_street_name', 'billing_street_number', 'billing_unit_number', 'billing_city', 'billing_province', 'billing_country', 'billing_postal', 'is_shipping_same_as_billing', 'shipping_phone', 'shipping_street_name', 'shipping_street_number', 'shipping_unit_number', 'shipping_city', 'shipping_province', 'shipping_country', 'shipping_postal', 'has_consented', 'user', 'profile', 'qrcode', 'is_tos_signed', 'is_verified', 'verification_key', 'date_of_birth', 'wants_newsletter', 'wants_flyers',)


class StoreSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization', read_only=True)
    header_url = serializers.URLField(source='header.image.url', read_only=True)
    logo_url = serializers.URLField(source='logo.image.url', read_only=True)
    class Meta:
        model = Store
        fields = ('store_id', 'name', 'description', 'joined', 'last_updated', 'is_suspended', 'is_listed', 'street_name', 'street_number', 'unit_number', 'city', 'province', 'country', 'postal', 'website', 'email', 'phone', 'fax', 'is_open_monday', 'is_open_tuesday', 'is_open_wednesday', 'is_open_thursday', 'is_open_friday', 'is_open_saturday', 'is_open_sunday', 'monday_to', 'tuesday_to', 'wednesday_to', 'thursday_to', 'friday_to', 'saturday_to', 'sunday_to', 'monday_from', 'tuesday_from', 'wednesday_from', 'thursday_from', 'friday_from', 'saturday_from', 'sunday_from', 'organization', 'employees', 'header', 'logo', 'tax_rate', 'currency', 'language', 'is_comics_vendor', 'is_furniture_vendor', 'is_coins_vendor', 'is_aggregated', 'organization_name', 'paypal_email', 'header_url', 'logo_url', 'style',)


class OrganizationSerializer(serializers.ModelSerializer):
    header_url = serializers.URLField(source='header.image.url', read_only=True)
    logo_url = serializers.URLField(source='logo.image.url', read_only=True)
    class Meta:
        model = Organization
        fields = ('org_id', 'name', 'description', 'joined', 'last_updated', 'is_suspended', 'is_listed', 'street_name', 'street_number', 'unit_number', 'city', 'province', 'country', 'postal', 'website', 'email', 'phone', 'fax', 'twitter', 'facebook_url', 'instagram_url', 'linkedin_url', 'github_url', 'google_url', 'youtube_url', 'flickr_url', 'administrator', 'header', 'logo','customers', 'currency', 'language', 'paypal_email', 'header_url', 'logo_url', 'style',)


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand', read_only=True)
    is_org_listed = serializers.CharField(source='organization.is_listed',read_only=True)
    is_store_listed = serializers.CharField(source='store.is_listed',read_only=True)
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'description', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'has_tax', 'tax_rate', 'tax_amount', 'sub_price_with_tax','discount', 'discount_type', 'price', 'cost', 'image', 'image_url', 'images', 'organization', 'store', 'section', 'brand', 'tags', 'is_listed', 'category', 'is_new', 'is_featured', 'qrcode', 'is_qrcode_printed', 'currency', 'language', 'has_no_shipping', 'brand_name', 'is_org_listed', 'is_store_listed',)


class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Employee
        fields = ('employee_id', 'role',  'joined', 'last_updated', 'is_suspended', 'user', 'organization', 'profile', 'first_name', 'last_name', 'email', 'is_tos_signed', 'is_verified', 'verification_key',)


class ComicSerializer(serializers.ModelSerializer):
    series_name = serializers.CharField(source='issue.series', read_only=True)
    issue_name = serializers.CharField(source='issue', read_only=True)
    class Meta:
        model = Comic
        fields = ('comic_id', 'is_cgc_rated', 'age',
                  'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', 'issue', 'catalog', 'product', 'created', 'organization', 'issue_name', 'series_name',
                  )


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('organization','store','employee','customer','receipt_id','created','last_updated','purchased','has_purchased_online','payment_method', 'sub_total', 'has_tax', 'tax_rate', 'tax_amount', 'sub_total_with_tax', 'discount_amount', 'shipping_amount', 'total_amount', 'has_finished', 'has_paid', 'status', 'email', 'billing_address', 'billing_phone', 'billing_city', 'billing_province', 'billing_country', 'billing_postal', 'shipping_address', 'shipping_phone', 'shipping_city', 'shipping_province', 'shipping_country', 'shipping_postal', 'products', 'has_error', 'error', 'has_shipping', 'comment',)


class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ('help_id', 'subject', 'subject_url', 'message', 'submission_date', 'screenshot', 'employee', 'store', 'organization',)


class ImageBinaryUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBinaryUpload
        fields = ('id', 'created', 'file_type', 'mime_type', 'owner', 'data',)


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('upload_id', 'upload_date', 'is_assigned', 'image', 'user',)


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('promotion_id', 'name', 'discount', 'discount_type', 'organization',)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section_id', 'name', 'store', 'organization')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        # Validate to ensure the user is not using an email which is banned in
        # our system for whatever reason.
        banned_domains = BannedDomain.objects.all()
        for banned_domain in banned_domains:
            if value.count(banned_domain.name) > 1:
                raise serializers.ValidationError("Email is using a banned domain.")
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class WishlistSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer', read_only=True)
    product_name = serializers.CharField(source='product', read_only=True)
    class Meta:
        model = Wishlist
        fields = ('wishlist_id', 'customer', 'product', 'created', 'customer_name', 'product_name',)


class PulllistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pulllist
        fields = ('pulllist_id', 'organization', 'store', 'series', )


class PulllistSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PulllistSubscription
        fields = ('subscription_id', 'pulllist', 'organization', 'customer', 'copies', 'created',)


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCDSeries
        fields = ('series_id', 'name', 'sort_name', 'format', 'color', 'dimensions', 'paper_stock', 'binding', 'publishing_format', 'tracking_notes', 'notes', 'publication_notes', 'keywords', 'year_began', 'year_ended', 'year_began_uncertain', 'year_ended_uncertain', 'publication_dates', 'has_barcode', 'has_indicia_frequency', 'has_isbn', 'has_issue_title', 'has_volume', 'created', 'has_rating', 'is_current', 'is_comics_publication', 'is_singleton', 'reserved', 'open_reserve', 'modified', 'deleted', 'country', 'language', 'publication_type_id', 'publisher', 'images', 'issue_count', 'has_gallery', 'publisher_name',)


class IssueSerializer(serializers.ModelSerializer):
    series_name = serializers.CharField(source='series', read_only=True)
    class Meta:
        model = GCDIssue
        fields = ('issue_id','number','title','no_title','volume','no_volume','display_volume_with_number','isbn','no_isbn','valid_isbn','variant_of_id','variant_name','barcode','no_barcode','rating','no_rating','is_first_issue','is_last_issue','publication_date','key_date','on_sale_date','on_sale_date_uncertain','sort_code','indicia_frequency','no_indicia_frequency','price','page_count','page_count_uncertain','editing','no_editing','notes','keywords','is_indexed','reserved','created','modified','deleted','indicia_pub_not_printed','no_brand','small_image','medium_image','large_image','alt_small_image','alt_medium_image','alt_large_image','has_alternative','brand','series','indicia_publisher','images','publisher_name', 'product_name', 'series_name',)


class StorySerializer(serializers.ModelSerializer):
    #series_name = serializers.CharField(source='series', read_only=True)
    class Meta:
        model = GCDStory
        fields = ('story_id', 'title', 'title_inferred', 'feature', 'type', 'sequence_number', 'page_count', 'page_count_uncertain', 'script', 'pencils', 'inks', 'colors', 'letters', 'editing', 'no_script', 'no_pencils', 'no_inks', 'no_colors', 'no_letters', 'no_editing', 'job_number', 'genre', 'characters', 'synopsis', 'reprint_notes', 'notes', 'keywords', 'issue', 'reserved', 'created', 'modified', 'deleted',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_id', 'name', 'discount', 'discount_type', 'organization',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('brand_id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'parent_id', 'name',)


class OrgShippingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgShippingPreference
        fields = ('shipping_pref_id','organization','is_pickup_only','rates')


class OrgShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgShippingRate
        fields = ('shipping_rate_id','organization','country','comics_rate1','comics_rate2','comics_rate3','comics_rate4','comics_rate5','comics_rate6','comics_rate7','comics_rate8','comics_rate9','comics_rate10',)


class StoreShippingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreShippingPreference
        fields = ('shipping_pref_id','organization','store','is_pickup_only','rates')


class StoreShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreShippingRate
        fields = ('shipping_rate_id','organization','store','country','comics_rate1','comics_rate2','comics_rate3','comics_rate4','comics_rate5','comics_rate6','comics_rate7','comics_rate8','comics_rate9','comics_rate10',)


class EmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ('subscription_id', 'email', 'submission_date', 'store', 'organization',)


class UnifiedShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnifiedShippingRate
        fields = ('shipping_rate_id','country','comics_rate1','comics_rate2','comics_rate3','comics_rate4','comics_rate5','comics_rate6','comics_rate7','comics_rate8','comics_rate9','comics_rate10',)


class PrintHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintHistory
        fields = ('print_id','created','filename','url','organization','store',)


class SubDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDomain
        fields = ('sub_domain_id','name','organization','store',)

    def validate_name(self, value):
        # Validate to ensure there are not capitals.
        if not value.islower():
            raise serializers.ValidationError("Your subdomain can only contain lowercase letters.")

        # Validate to ensure there are no special characters (including whitespace).
        if not value.isalpha():
            raise serializers.ValidationError("Your subdomain cannot have special characters.")

        # Validate to ensure the user doesn't take a valuable sub-domain name
        # that we (ComicsCantina) can use in the future.
        reserved_words = [
            'dev','develop', 'development', 'developments', 'developer',
            'qa','quality', 'qualityassurance', 'developments', 'book', 'books',
            'prod','production', 'productions', 'shop', 'shops', 'docgen',
            'img', 'image', 'images', 'shopping', 'comicbooks', 'comicbook',
            'help', 'contact', 'contactus', 'exchange', 'stock', 'product',
            'products', 'list', 'listing', 'listings', 'directory', 'tech',
            'technology', 'engineer', 'engineering', 'landpage', 'page', 'test',
            'tests', 'testing', 'doc', 'docs', 'document', 'documents',
            'file', 'files', 'ftp', 'sftp', 'server', 'client', 'comic',
            'comics', 'issue', 'issues', 'series', 'publisher', 'publishers',
            'brand', 'brands', 'inv', 'inventory', 'inventorying', 'catalog',
            'inventorys', 'catalogs', 'ios','android','microsoft', 'apple',
            'samsung', 'mobile', 'tablet', '', 'iphone', 'reader', 'reading',
            'download', 'downloader', 'downloading', 'news', 'blogs', 'www',
            'tutorial', 'tutorials', 'edu', 'education', 'educational', 'link',
            'article', 'www2', 'ww3', 'ww4', 'store', 'storing', 'start', 'begin',
            'checkout', 'pos', 'api', 'ssh', 'buy', 'learn', 'discover',
            'discovery',
        ]
        if value in reserved_words:
            raise serializers.ValidationError("Cannot us a reserved name")

        # Validate to ensure the domain name isn't using a 'bad word'.
        bad_words = BannedWord.objects.all()
        if value in bad_words:
            raise serializers.ValidationError("Cannot us that word!")

        # Return the successfully validated value.
        return value


class BannedDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedDomain
        fields = ('id','name','banned_on','reason',)


class BannedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedIP
        fields = ('id','address','banned_on','reason',)


class BannedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedWord
        fields = ('id','text','banned_on','reason',)


class CatalogItemSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source='image.image.url', read_only=True)
    class Meta:
        model = CatalogItem
        fields = ('catalog_id','name','type','description','brand_name','image','image_url','created','last_updated','length_in_meters','width_in_meters','height_in_meters','weight_in_kilograms','volume_in_litres','materials','is_tangible','is_flammable','is_biohazard','is_toxic','is_explosive','is_corrosive','is_volatile','is_radioactive','is_restricted','restrictions','organization', 'store',)
