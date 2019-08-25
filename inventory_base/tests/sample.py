#import json
from datetime import datetime
#from django.core.urlresolvers import resolve
#from django.http import HttpRequest
#from django.http import QueryDict
#from django.test import TestCase
#from django.test import Client
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from captcha.models import CaptchaStore
from django.db import IntegrityError, transaction
from ecantina_project import constants

# Grand Comics Database Models
#------------------------------------------------------------------
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.branduse import GCDBrandUse
from api.models.gcd.brandemblemgroup import GCDBrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.helprequest import HelpRequest
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.product import Product
from api.models.ec.promotion import Promotion
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.models.ec.receipt import Receipt
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.tag import Tag
from api.models.ec.wishlist import Wishlist


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"


class SampleDataPopulator():
    def populate(self):
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self.run_populate()
        except IntegrityError:
            pass

    def dealloc(self):
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self.run_dealloc()
        except IntegrityError:
            pass

    def run_dealloc(self):
        for customer in Customer.objects.all():
            customer.delete()
        for image in ImageUpload.objects.all():
            image.delete()
        for org in Organization.objects.all():
            org.delete()
        for store in Store.objects.all():
            store.delete()
        for employee in Employee.objects.all():
            employee.delete()
        for section in Section.objects.all():
            section.delete()
        for product in Product.objects.all():
            product.delete()
        for comic in Comic.objects.all():
            comic.delete()
        User.objects.all().delete()

    def run_populate(self):
        now = datetime.now()
        pass

        #----------------
        # Administrator
       #----------------
        try:
            user = User.objects.create_user(
                TEST_USER_EMAIL,  # Username
                TEST_USER_EMAIL,  # Email
                TEST_USER_PASSWORD,
            )
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except Exception as e:
            user = User.objects.get(email=TEST_USER_EMAIL)
        try:
            user2 = User.objects.create_user(
                "Hideauze",  # Username
                "Hideauze1@evolvers.com",  # Email
                TEST_USER_PASSWORD,
            )
            user2.is_active = True
            user2.save()
        except Exception as e:
            user2 = User.objects.get(email="Hideauze1@evolvers.com")

        #----------------
        # Image Uploads
        #----------------
        logo = None
        profile = None

        #-----------------
        # Customer
        #-----------------
        try:
            customer1 = Customer.objects.create(
                customer_id = 1,
                                                
                # Name & Contact
                first_name = 'Rei',
                last_name = ' Ayanami',
                email = 'rayanami@nerv.worldgov',
                                                
                # Billing Info
                billing_phone = '111-111-1111',
                email = 'rayanami@nerv.worldgov',
                billing_street_name = 'Nerv HQ Street',
                billing_street_number = '1000',
                billing_unit_number = '666',
                billing_city = 'Neo Tokyo',
                billing_province = 'Shinjuku',
                billing_country = 'Japan',
                billing_postal = 'N6J4X4',
                
                # Shipping Info
                shipping_phone = '111-111-1111',
                shipping_street_name = 'Nerv HQ Street',
                shipping_street_number = '1000',
                shipping_unit_number = '666',
                shipping_city = 'Neo Tokyo',
                shipping_province = 'Shinjuku',
                shipping_country = 'Japan',
                shipping_postal = 'N6J4X4',
                                                
                # Legal
                has_consented = True,
                
                # References.
                user = user2,
                profile = profile,
            )
        except Exception as e:
            print("Failed creating customer 1")
            customer1 = Customer.objects.get(user=user2)

        #-----------------
        # Organization
        #-----------------
        try:
            organization = Organization.objects.create(
                org_id=1,
                name='B.A.\'s Comics',
                description = 'Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
                street_name='Hamilton Rd',
                street_number='426',
                unit_number=None,
                city='London',
                province='Ontario',
                country='Canada',
                postal='N5Z 1R9',
                website='http://www.bacomics.ca',
                email=None,
                phone='519-439-9636',
                fax=None,
                twitter='https://twitter.com/bascomics',
                facebook_url=None,
                instagram_url=None,
                linkedin_url=None,
                github_url=None,
                google_url='https://plus.google.com/105760942218297346537/about',
                youtube_url=None,
                flickr_url=None,
                administrator = user,
                logo = logo,
            )
            organization.customers.add(customer)
        except Exception as e:
            organization = Organization.objects.get(org_id=1)

        #-----------------
        # Store
        #-----------------
        try:
            store = Store.objects.create(
                store_id=1,
                name='Main Store',
                description='Located in London, Ontario, BA\’s Comics and Nostalgia is operated by Bruno Andreacchi, an industry veteran with over 30 years experience in grading, curating, and offering Comic Books and Graphic Novels. Bruno first began collecting in the 1960s, and since then has gone on to become an industry expert, writing articles for several key industry publications, such as Wizard.',
                street_name='Hamilton Rd',
                street_number='426',
                unit_number=None,
                city='London',
                province='Ontario',
                country='Canada',
                postal='N5Z 1R9',
                website='http://www.bacomics.ca',
                email=None,
                phone='519-439-9636',
                fax=None,
                organization=organization,
            )
        except Exception as e:
            store = Store.objects.get(store_id=1)

        #-----------------
        # Sections
        #-----------------
        sections = Section.objects.filter(store=store)
        if len(sections) is 0:
            Section.objects.create(
                section_id=1,
                name='Downstairs',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=2,
                name='Upstairs',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=3,
                name='Front Pile',
                store=store,
                organization = organization,
            )
            Section.objects.create(
                section_id=4,
                name='Back Pile',
                store=store,
                organization = organization,
            )

        #-----------------
        # Employees
        #-----------------
        try:
            employee = Employee.objects.create(
                employee_id=1,
                street_name = 'Centre Street',
                street_number = '120',
                unit_number = '102',
                city = 'London',
                province = 'Ontario',
                country = 'Canada',
                postal = 'N6J4X4',
                email = 'bmika@icloud.com',
                phone = '519-432-7898',
                role = constants.EMPLOYEE_OWNER_ROLE,
                user = user,
                organization = organization,
                profile=profile,
            )
        except Exception as e:
            employee = Employee.objects.get(Employee_id=1)

        #-----------
        # Country
        #----------
        try:
            country = GCDCountry.objects.create(
                 country_id=1,
                 code='ca',
                 name='Canada',
            )
        except Exception as e:
            country = GCDCountry.objects.get(country_id=1)

        #------------
        # Language
        #-----------
        try:
            language = GCDLanguage.objects.create(
                language_id=1,
                code='En',
                name='English',
            )
        except Exception as e:
            language = GCDLanguage.objects.get(language_id=1)

        #-----------------
        # Publisher
        #-----------------
        try:
            publisher = GCDPublisher.objects.create(
                publisher_id=1,
                name='Lucha Comics',
                year_began='2015',
            #year_ended=year_ended,
            #notes=notes,
            #url=url,
            #is_master=is_master,
            ## parent_id
            #imprint_count=imprint_count,
            #brand_count=brand_count,
            #indicia_publisher_count=indicia_publisher_count,
            #series_count=series_count,
            #created=created,
            #modified=modified,
            #issue_count=issue_count,
            #reserved=reserved,
            #deleted=deleted,
            #year_began_uncertain=year_began_uncertain,
            #year_ended_uncertain=year_ended_uncertain,
                country=country,
            )
        except Exception as e:
            publisher = GCDPublisher.objects.get(publisher_id=1)

        #-----------------
        # Series
        #-----------------
        try:
            series = GCDSeries.objects.create(
                series_id=1,
                name='Winterworld',
                sort_name='Winterworld',
                #format=format,
                year_began='2015',
                year_ended='3000',
                #year_began_uncertain=year_began_uncertain,
                #year_ended_uncertain=year_ended_uncertain,
                #publication_dates=publication_dates,
                #is_current=is_current,
                publisher=publisher,
                country=country,
                language=language,
                #tracking_notes=tracking_notes,
                #notes=notes,
                #publication_notes=publication_notes,
                #has_gallery=has_gallery,
                #open_reserve=open_reserve,
                #issue_count=issue_count,
                #created=created,
                #modified=modified,
                #reserved=reserved,
                #deleted=deleted,
                #has_indicia_frequency=has_indicia_frequency,
                #has_isbn=has_isbn,
                #has_barcode=has_barcode,
                #has_issue_title=has_issue_title,
                #has_volume=has_volume,
                #is_comics_publication=is_comics_publication,
                #color=color,
                #dimensions=dimensions,
                #paper_stock=paper_stock,
                #binding=binding,
                #publishing_format=publishing_format,
                #has_rating=has_rating,
                #publication_type_id=publication_type_id,
                #is_singleton=is_singleton,
            )
        except Exception as e:
            series = GCDSeries.objects.get(series_id=1)

        #-----------------
        # Issue
        #-----------------
        try:
            issue = GCDIssue.objects.create(
                issue_id=1,
                number='1',
                volume='1',
                #no_volume=False,
                #display_volume_with_number=True,
                series = series,
                #indicia_publisher = None,
                #indicia_pub_not_printed = True,
                #brand = None,
                #no_brand = True,
                #publication_date = 'December 9',
                #key_date = key_date,
                sort_code = '0',
                #price = price,
                #page_count = page_count,
                #page_count_uncertain = page_count_uncertain,
                #indicia_frequency = indicia_frequency,
                #no_indicia_frequency = no_indicia_frequency,
                #editing = editing,
                #no_editing = no_editing,
                #notes = notes,
                #created = created,
                #modified = modified,
                #reserved = reserved,
                #deleted = deleted,
                #is_indexed = is_indexed,
                #isbn = isbn,
                #valid_isbn = valid_isbn,
                #no_isbn = no_isbn,
                #variant_of_id = variant_of_id,
                #variant_name = variant_name,
                #barcode = barcode,
                #no_barcode = no_barcode,
                title = 'Winterworld',
                #no_title = no_title,
                #on_sale_date = on_sale_date,
                #on_sale_date_uncertain = on_sale_date_uncertain,
                #rating = rating,
                #no_rating = no_rating,
            )
        except Exception as e:
            issue = Issue.objects.get(issue_id=1)

        #-----------------
        # Pull List
        #-----------------
        try:
            pulllist = Pulllist.objects.create(
                pulllist_id = 1,
                organization = organization,
                store = store,
                series = series,
            )
        except Exception as e:
            pulllist = Pulllist.objects.get(pulllist_id=1)

        #------------------------
        # Pull List Subscription
        #------------------------
        try:
            pullistsubscription = PulllistSubscription.objects.create(
                subscription_id = 1,
                organization = organization,
                pulllist = pulllist,
                customer = customer1,
                copies = 2,
            )
        except Exception as e:
            pullistsubscription = PulllistSubscription.objects.get(subscription_id=1)

        #------------------------
        # Receipt
        #------------------------
        try:
            receipt = Receipt.objects.create(
                organization = organization,
                store = store,
                employee = employee,
                customer = customer1,
                receipt_id = 1,
                #created =
                #last_updated =
                has_purchased_online = False,
                payment_method = 1,
                status = 1,
                sub_total = 10.0,
                discount_amount = 1,
                has_tax = True,
                tax_rate = 0.13,
                tax_amount = 1,
                total_amount = 10,
                has_finished = False,
                has_paid = False,
                billing_address = '102-120 Centre Street',
                email = 'rayanami@nerv.worldgov',
                billing_phone = '111-111-1111',
                billing_city = 'London',
                billing_province = 'Ontario',
                billing_country = 'Canada',
                billing_postal = 'N6J4X4',
                shipping_address = '102-120 Centre Street',
                shipping_phone = '111-111-1111',
                shipping_city = 'London',
                shipping_province = 'Ontario',
                shipping_country = 'Canada',
                shipping_postal = 'N6J4X4',
            )
        except Exception as e:
            receipt = Receipt.objects.get(recepit_id=1)
