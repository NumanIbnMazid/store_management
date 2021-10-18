from django.contrib.auth import get_user_model
from customers.models import Customer
from staffs.models import Staff
from studios.models import Studio, VatTax, Currency
from stores.models import Store, StoreModerator, CustomBusinessDay
from spaces.models import Space
from plans.models import Plan, OptionCategory, Option
from deals.models import Coupon, PointSetting


import factory
from factory.django import DjangoModelFactory
import random


# Defining a factory

# *** User ***

class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    name = factory.Faker("first_name")
    email = factory.Faker("email")


# Using a factory with auto-generated data
# user = UserFactory()


# *** Customer ***

class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)


# Using a factory with auto-generated data
# customer = CustomerFactory()


# *** Staff ***

class StaffFactory(DjangoModelFactory):
    class Meta:
        model = Staff

    user = factory.SubFactory(UserFactory)


# Using a factory with auto-generated data
# staff = StaffFactory()


# *** Studio ***

class StudioFactory(DjangoModelFactory):
    class Meta:
        model = Studio

    user = factory.SubFactory(UserFactory)


# Using a factory with auto-generated data
# studio = StudioFactory()


# *** VatTax ***

class VatTaxFactory(DjangoModelFactory):
    class Meta:
        model = VatTax

    studio = factory.SubFactory(StudioFactory)


# Using a factory with auto-generated data
# vattax = VatTaxFactory()


# *** VatTax ***

class CurrencyFactory(DjangoModelFactory):
    class Meta:
        model = Currency

    studio = factory.SubFactory(StudioFactory)


# Using a factory with auto-generated data
# currency = CurrencyFactory()


# *** Store ***

class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store
        django_get_or_create = ('name',)

    studio = factory.SubFactory(StudioFactory)
    name = factory.Sequence(lambda n: 'Store {0}'.format(n))
    default_closed_day_of_weeks = [random.choice([
        "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    ])]


# Using a factory with auto-generated data
# store = StoreFactory()


# *** StoreModerator ***

class StoreModeratorFactory(DjangoModelFactory):
    class Meta:
        model = StoreModerator

    user = factory.SubFactory(UserFactory)
    
    @factory.post_generation
    def store(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.store.add(*extracted)


# Using a factory with auto-generated data
# store_moderator = StoreModeratorFactory()


# *** CustomBusinessDay ***

class CustomBusinessDayFactory(DjangoModelFactory):
    class Meta:
        model = CustomBusinessDay

    store = factory.SubFactory(StoreFactory)
    date = factory.Faker("date")


# Using a factory with auto-generated data
# custom_business_day = CustomBusinessDayFactory()


# *** Space ***

class SpaceFactory(DjangoModelFactory):
    class Meta:
        model = Space

    store = factory.SubFactory(StoreFactory)


# Using a factory with auto-generated data
# space = SpaceFactory()


# *** OptionCategory ***

class OptionCategoryFactory(DjangoModelFactory):
    class Meta:
        model = OptionCategory

    studio = factory.SubFactory(StudioFactory)


# Using a factory with auto-generated data
# option_category = OptionCategoryFactory()


# *** OptionCategory ***

class OptionFactory(DjangoModelFactory):
    class Meta:
        model = Option

    option_category = factory.SubFactory(OptionCategoryFactory)


# Using a factory with auto-generated data
# option = OptionFactory()


# *** Plan ***

class PlanFactory(DjangoModelFactory):
    class Meta:
        model = Plan

    @factory.post_generation
    def space(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.space.add(*extracted)
    
    @factory.post_generation
    def option(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.option.add(*extracted)


# Using a factory with auto-generated data
# plan = PlanFactory()


# *** Coupon ***

class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    studio = factory.SubFactory(StudioFactory)


# Using a factory with auto-generated data
# coupon = CouponFactory()


# *** PointSetting ***

class PointSettingFactory(DjangoModelFactory):
    class Meta:
        model = PointSetting

    studio = factory.SubFactory(StudioFactory)


# Using a factory with auto-generated data
# point_setting = PointSettingFactory()

