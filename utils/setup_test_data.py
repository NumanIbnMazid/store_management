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

NUM_USER = 7
NUM_CUSTOMER = 7
NUM_STAFF = 7
NUM_STUDIO = 7
NUM_VATTAX = 7
NUM_CURRENCY = 7
NUM_STORE = 7
NUM_STORE_MODERATOR = 7
NUM_CUSTOM_BUSINESS_DAY = 7
NUM_SPACE = 7
NUM_OPTION_CATEGORY = 7
NUM_OPTION = 7
NUM_PLAN = 7
NUM_COUPON = 7
NUM_POINT_SETTING = 7


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [
            get_user_model(), Customer, Staff, Studio, VatTax, Currency, Store, StoreModerator, CustomBusinessDay, Space, Plan, OptionCategory, Option, Coupon, PointSetting
        ]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        
        # Create all the users
        users = []
        for _ in range(NUM_USER):
            user = UserFactory()
            users.append(user)
        
        # Create all the customers
        customers = []
        for _ in range(NUM_CUSTOMER):
            customer = CustomerFactory()
            customers.append(customer)
        
        # Create all the staffs
        staffs = []
        for _ in range(NUM_STAFF):
            data = StaffFactory()
            staffs.append(data)
        
        # Create all the studios
        studios = []
        for _ in range(NUM_STUDIO):
            data = StudioFactory()
            studios.append(data)
        
        # Create all the vattax
        vattax = []
        for _ in range(NUM_VATTAX):
            data = VatTaxFactory()
            vattax.append(data)
        
        # Create all the currencies
        currencies = []
        for _ in range(NUM_CURRENCY):
            data = CurrencyFactory()
            currencies.append(data)
        
        # Create all the stores
        stores = []
        for _ in range(NUM_STORE):
            data = StoreFactory()
            stores.append(data)
        
        # Create all the store_moderators
        store_moderators = []
        for _ in range(NUM_STORE_MODERATOR):
            data = StoreModeratorFactory()
            store_moderators.append(data)
        
        # Create all the custom_business_days
        custom_business_days = []
        for _ in range(NUM_CUSTOM_BUSINESS_DAY):
            data = CustomBusinessDayFactory()
            custom_business_days.append(data)
        
        # Create all the spaces
        spaces = []
        for _ in range(NUM_SPACE):
            data = SpaceFactory()
            spaces.append(data)
        
        # Create all the option_categories
        option_categories = []
        for _ in range(NUM_OPTION_CATEGORY):
            data = OptionCategoryFactory()
            option_categories.append(data)
        
        # Create all the options
        options = []
        for _ in range(NUM_OPTION):
            data = OptionFactory()
            options.append(data)
        
        # Create all the plans
        plans = []
        for _ in range(NUM_PLAN):
            data = PlanFactory()
            plans.append(data)
        
        # Create all the coupons
        coupons = []
        for _ in range(NUM_COUPON):
            data = CouponFactory()
            coupons.append(data)
        
        # Create all the point_settings
        point_settings = []
        for _ in range(NUM_POINT_SETTING):
            data = PointSettingFactory()
            point_settings.append(data)
