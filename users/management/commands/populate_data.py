from django.contrib.auth import get_user_model
from customers.models import Customer
from staffs.models import Staff
from studios.models import Studio, VatTax, Currency
from stores.models import Store, StoreModerator, CustomBusinessDay
from spaces.models import Space
from plans.models import Plan, OptionCategory, Option
from deals.models import Coupon, PointSetting
from utils.factories import (
    UserFactory,
    CustomerFactory,
    StaffFactory,
    StudioFactory,
    VatTaxFactory,
    CurrencyFactory,
    StoreFactory,
    StoreModeratorFactory,
    CustomBusinessDayFactory,
    SpaceFactory,
    OptionCategoryFactory,
    OptionFactory,
    PlanFactory,
    CouponFactory,
    PointSettingFactory,
)

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone

DEFAULT_NUM_OF_DATA = 7

NUM_USER = DEFAULT_NUM_OF_DATA
NUM_CUSTOMER = DEFAULT_NUM_OF_DATA
NUM_STAFF = DEFAULT_NUM_OF_DATA
NUM_STUDIO = DEFAULT_NUM_OF_DATA
NUM_VATTAX = DEFAULT_NUM_OF_DATA
NUM_CURRENCY = DEFAULT_NUM_OF_DATA
NUM_STORE = DEFAULT_NUM_OF_DATA
NUM_STORE_MODERATOR = DEFAULT_NUM_OF_DATA
NUM_CUSTOM_BUSINESS_DAY = DEFAULT_NUM_OF_DATA
NUM_SPACE = DEFAULT_NUM_OF_DATA
NUM_OPTION_CATEGORY = DEFAULT_NUM_OF_DATA
NUM_OPTION = DEFAULT_NUM_OF_DATA
NUM_PLAN = DEFAULT_NUM_OF_DATA
NUM_COUPON = DEFAULT_NUM_OF_DATA
NUM_POINT_SETTING = DEFAULT_NUM_OF_DATA


class Command(BaseCommand):
    help = "Generates test data"
    
    def _delete_old_data(self):
        self.stdout.write("Deleting old data...")
        models = [
            get_user_model(), Customer, Staff, Studio, VatTax, Currency, Store, StoreModerator, CustomBusinessDay, Space, Plan, OptionCategory, Option, Coupon, PointSetting
        ]
        for m in models:
            m.objects.all().delete()
            
    def _create_admin_users(self):
        self.stdout.write("Creating admin users...")
        # Default Users
        if not get_user_model().objects.filter(email__iexact='admin@admin.com').exists():
            u_admin = get_user_model()(email='admin@admin.com')
            u_admin.set_password("admin")
            u_admin.is_staff = True
            u_admin.is_superuser = True
            u_admin.save()
    
    def _create_new_data(self):
        self.stdout.write("Creating new data...")
        # users
        self._create_users_data()
        # customers
        self._create_customers_data()
        # staffs
        self._create_staffs_data()
        # studios
        self._create_studios_data()
        # vattax
        self._create_vattax_data()
        # currencies
        self._create_currencies_data()
        # stores
        self._create_stores_data()
        # store_moderators
        self._create_store_moderators_data()
        # custom_business_days
        self._create_custom_business_days_data()
        # spaces
        self._create_spaces_data()
        # option_categories
        self._create_option_categories_data()
        # options
        self._create_options_data()
        # plans
        self._create_plans_data()
        # coupons
        self._create_coupons_data()
        # point_settings
        self._create_point_settings_data()
        
    def _create_users_data(self):
        self.stdout.write("Creating users...")
        # Create all the users
        users = []
        for _ in range(NUM_USER):
            user = UserFactory()
            users.append(user)
        
    def _create_customers_data(self):
        self.stdout.write("Creating customers...")
        # Create all the customers
        customers = []
        for _ in range(NUM_CUSTOMER):
            customer = CustomerFactory()
            customers.append(customer)
        
    def _create_staffs_data(self):
        self.stdout.write("Creating staffs...")
        # Create all the staffs
        staffs = []
        for _ in range(NUM_STAFF):
            data = StaffFactory()
            staffs.append(data)
        
    def _create_studios_data(self):
        self.stdout.write("Creating studios...")
        # Create all the studios
        studios = []
        for _ in range(NUM_STUDIO):
            data = StudioFactory()
            studios.append(data)
        
    def _create_vattax_data(self):
        self.stdout.write("Creating vattax...")
        # Create all the vattax
        vattax = []
        for _ in range(NUM_VATTAX):
            data = VatTaxFactory()
            vattax.append(data)
        
    def _create_currencies_data(self):
        self.stdout.write("Creating currencies...")
        # Create all the currencies
        currencies = []
        for _ in range(NUM_CURRENCY):
            data = CurrencyFactory()
            currencies.append(data)
        
    def _create_stores_data(self):
        self.stdout.write("Creating stores...")
        # Create all the stores
        stores = []
        for _ in range(NUM_STORE):
            data = StoreFactory()
            stores.append(data)
        
    def _create_store_moderators_data(self):
        self.stdout.write("Creating store moderators...")
        # Create all the store_moderators
        store_moderators = []
        for _ in range(NUM_STORE_MODERATOR):
            data = StoreModeratorFactory()
            store_moderators.append(data)
        
    def _create_custom_business_days_data(self):
        self.stdout.write("Creating custom business days...")
        # Create all the custom_business_days
        custom_business_days = []
        for _ in range(NUM_CUSTOM_BUSINESS_DAY):
            data = CustomBusinessDayFactory()
            custom_business_days.append(data)
        
    def _create_spaces_data(self):
        self.stdout.write("Creating spaces...")
        # Create all the spaces
        spaces = []
        for _ in range(NUM_SPACE):
            data = SpaceFactory()
            spaces.append(data)
        
    def _create_option_categories_data(self):
        self.stdout.write("Creating option categories...")
        # Create all the option_categories
        option_categories = []
        for _ in range(NUM_OPTION_CATEGORY):
            data = OptionCategoryFactory()
            option_categories.append(data)
        
    def _create_options_data(self):
        self.stdout.write("Creating options...")
        # Create all the options
        options = []
        for _ in range(NUM_OPTION):
            data = OptionFactory()
            options.append(data)
        
    def _create_plans_data(self):
        self.stdout.write("Creating plans...")
        # Create all the plans
        plans = []
        for _ in range(NUM_PLAN):
            data = PlanFactory()
            plans.append(data)
        
    def _create_coupons_data(self):
        self.stdout.write("Creating coupons...")
        # Create all the coupons
        coupons = []
        for _ in range(NUM_COUPON):
            data = CouponFactory()
            coupons.append(data)
        
    def _create_point_settings_data(self):
        self.stdout.write("Creating point settings...")
        # Create all the point_settings
        point_settings = []
        for _ in range(NUM_POINT_SETTING):
            data = PointSettingFactory()
            point_settings.append(data)
        

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # delete old data
        self._delete_old_data()
        # create admin users
        self._create_admin_users()
        # create new data
        self._create_new_data()



# Command for testing

# class Command(BaseCommand):
#     help = 'Displays current time'

#     def handle(self, *args, **kwargs):
#         time = timezone.now().strftime('%X')
#         self.stdout.write("It's now %s" % time)
