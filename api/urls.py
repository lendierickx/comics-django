from django.conf.urls import url, include
from api.views import imagebinaryupload
from api.views import comic
from api.views import customer
from api.views import organization
from api.views import store
from api.views import product
from api.views import employee
from api.views import receipt
from api.views import helprequest
from api.views import imageupload
from api.views import promotion
from api.views import section
from api.views import user
from api.views import wishlist
from api.views import pulllist
from api.views import pulllistsubscription
from api.views import series
from api.views import issue
from api.views import story
from api.views import tag
from api.views import category
from api.views import brand
from api.views import orgshippingpreference
from api.views import orgshippingrate
from api.views import emailsubscription
from api.views import unifiedshippingrate
from api.views import print_history
from api.views import subdomain
from api.views import banned_domain
from api.views import banned_ip
from api.views import banned_word
from api.views import register
from api.views import login
from api.views import catalog_item
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'imagebinaryuploads', imagebinaryupload.ImageBinaryUploadViewSet)
router.register(r'comics', comic.ComicViewSet)
router.register(r'organizations', organization.OrganizationViewSet)
router.register(r'customers', customer.CustomerViewSet)
router.register(r'stores', store.StoreViewSet)
router.register(r'products', product.ProductViewSet)
router.register(r'employees', employee.EmployeeViewSet)
router.register(r'receipts', receipt.ReceiptViewSet)
router.register(r'helprequests', helprequest.HelpRequestViewSet)
router.register(r'imageuploads', imageupload.ImageUploadViewSet)
router.register(r'promotions', promotion.PromotionViewSet)
router.register(r'tags', tag.TagViewSet)
router.register(r'sections', section.SectionViewSet)
router.register(r'users', user.UserViewSet)
router.register(r'groups', user.GroupViewSet)
router.register(r'wishlists', wishlist.WishlistViewSet)
router.register(r'pulllists', pulllist.PulllistViewSet)
router.register(r'pulllistsubscriptions', pulllistsubscription.PulllistSubscriptionViewSet)
router.register(r'series', series.SeriesViewSet)
router.register(r'issues', issue.IssueViewSet)
router.register(r'stories', story.StoryViewSet)
router.register(r'categories', category.CategoryViewSet)
router.register(r'brands', brand.BrandViewSet)
router.register(r'orgshippingpreferences', orgshippingpreference.OrgShippingPreferenceViewSet)
router.register(r'orgshippingrates', orgshippingrate.OrgShippingRateViewSet)
router.register(r'emailsubscriptions', emailsubscription.EmailSubscriptionViewSet)
router.register(r'unifiedshippingrates', unifiedshippingrate.UnifiedShippingRateViewSet)
router.register(r'print_history', print_history.PrintHistoryViewSet)
router.register(r'subdomains', subdomain.SubDomainViewSet)
router.register(r'banned_domains', banned_domain.BannedDomainViewSet)
router.register(r'banned_ips', banned_ip.BannedIPViewSet)
router.register(r'banned_words', banned_word.BannedWordViewSet)
router.register(r'banned_words', banned_word.BannedWordViewSet)
router.register(r'registers', register.RegisterViewSet)
router.register(r'logins', login.LoginViewSet)
router.register(r'catalog_items', catalog_item.CatalogItemViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]