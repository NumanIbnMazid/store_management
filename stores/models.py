from django.db import models
from utils.image_upload_helper import upload_store_image_path
from utils.helpers import model_cleaner
from studios.models import Studio
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from utils.helpers import autoslugFromUUID
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@autoslugFromUUID()
class Store(models.Model):
    
    name = models.CharField(max_length=150)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_stores")
    slug = models.SlugField(unique=True, max_length=254)
    default_closed_day_of_weeks = ArrayField(models.CharField(max_length=254), blank=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    contact_1 = models.CharField(max_length=30, blank=True, null=True)
    contact_2 = models.CharField(max_length=30, blank=True, null=True)
    explanatory_comment = models.CharField(max_length=254, blank=True, null=True)
    google_map = models.TextField(blank=True, null=True)
    image_1 = models.ImageField(upload_to=upload_store_image_path, blank=True, null=True)
    image_1_reference = models.CharField(max_length=254, blank=True, null=True)
    image_1_comment = models.CharField(max_length=254, blank=True, null=True)
    image_2 = models.ImageField(upload_to=upload_store_image_path, blank=True, null=True)
    image_2_reference = models.CharField(max_length=254, blank=True, null=True)
    image_2_comment = models.CharField(max_length=254, blank=True, null=True)
    image_3 = models.ImageField(upload_to=upload_store_image_path, blank=True, null=True)
    image_3_reference = models.CharField(max_length=254, blank=True, null=True)
    image_3_comment = models.CharField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    
    def clean(self, initialObject=None, requestObject=None):
        studio_id = initialObject.studio.id if initialObject else self.studio.id if self.studio else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower(), studio__id=studio_id),
                "field": "name"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)
        
    def get_business_day_status_from_datetime(self, datetimeInReq):
        result = {
            "store": self.name,
            "datetime": datetimeInReq.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": datetimeInReq.strftime("%A"),
            "status": "closed"
        }
        
        dateStr = datetimeInReq.strftime("%Y-%m-%d")
        timeObj = datetimeInReq.time()
        day_of_week = datetimeInReq.strftime("%A")
        
        IS_BUSINESS_DAY = False
        
        custom_business_day_qs = CustomBusinessDay.objects.filter(
            date=dateStr, status=0, store__slug=self.slug
        )
        
        # case 1: Exists in default closed day but open in custom business day :-> open
        if day_of_week in self.default_closed_day_of_weeks:
            custom_business_day_qs = CustomBusinessDay.objects.filter(
                date=dateStr, status=1, store__slug=self.slug
            )
            if custom_business_day_qs:
                IS_BUSINESS_DAY = True
        
        # case 2: Not exists in default closed day and not exists in custom business day :-> open
        elif day_of_week not in self.default_closed_day_of_weeks:
            custom_business_day_qs = CustomBusinessDay.objects.filter(
                date=dateStr, status=0, store__slug=self.slug
            )
            if not custom_business_day_qs:
                IS_BUSINESS_DAY = True
        
        else:
            pass
        
        if IS_BUSINESS_DAY:
            store_business_hour_from_day_of_week = self.store_business_hour.get_business_hour_from_day_of_week(
                day_of_week=day_of_week
            )
            opening_time = store_business_hour_from_day_of_week["opening_time"]
            closing_time = store_business_hour_from_day_of_week["closing_time"]
            
            is_open = False
            
            if opening_time <= closing_time:
                is_open =  opening_time <= timeObj <= closing_time
            else:
                is_open = opening_time <= timeObj or timeObj <= closing_time
            
            # alter is open status
            if is_open:
                result["status"] = "open"
        
        return result
        

@autoslugFromUUID()
class StoreModerator(models.Model):
    
    user = models.OneToOneField(get_user_model(), related_name='store_moderator_user', on_delete=models.CASCADE)
    store = models.ManyToManyField(Store, related_name="store_moderators")
    slug = models.SlugField(unique=True, max_length=254)
    contact = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Store Moderator'
        verbose_name_plural = 'Store Moderators'
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.get_dynamic_username()
    
    def clean(self, initialObject=None, requestObject=None):
        pass
    
    def get_stores(self):
        store_ids = [st.id for st in self.store.all()]
        return store_ids
    

@autoslugFromUUID()
class CustomBusinessDay(models.Model):
    class Status(models.IntegerChoices):
        CLOSED = 0, _("Closed")
        OPEN = 1, _("Open")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_custom_business_days")
    slug = models.SlugField(unique=True, max_length=254)
    date = models.DateField()
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Store Custom Business Day'
        verbose_name_plural = 'Store Custom Business Days'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.date)
    
    def clean(self, initialObject=None, requestObject=None):
        store_id = initialObject.store.id if initialObject else self.store.id if self.store else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(date=self.date, store__id=store_id),
                "field": "date"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)
    
    def get_status_str(self):
        if self.status == 0:
            return "Closed"
        return "Open"
    
    def get_business_day_type(self):
        if self.status == 0:
            return "custom_closed_day"
        elif self.status == 1:
            return "custom_business_day"
        return "default_business_day"


@autoslugFromUUID()
class StoreBusinessHour(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="store_business_hour")
    slug = models.SlugField(unique=True, max_length=254)
    saturday_opening_time = models.TimeField()
    saturday_closing_time = models.TimeField()
    sunday_opening_time = models.TimeField()
    sunday_closing_time = models.TimeField()
    monday_opening_time = models.TimeField()
    monday_closing_time = models.TimeField()
    tuesday_opening_time = models.TimeField()
    tuesday_closing_time = models.TimeField()
    wednesday_opening_time = models.TimeField()
    wednesday_closing_time = models.TimeField()
    thursday_opening_time = models.TimeField()
    thursday_closing_time = models.TimeField()
    friday_opening_time = models.TimeField()
    friday_closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Store Business Hour'
        verbose_name_plural = 'Store Business Hours'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.store.name)
    
    def clean(self, initialObject=None, requestObject=None):
        pass
    
    def get_business_hour_from_day_of_week(self, day_of_week):
        result = {
            "opening_time": None,
            "closing_time": None
        }
        if day_of_week == "Saturday":
            result["opening_time"] = self.saturday_opening_time
            result["closing_time"] = self.saturday_closing_time
        
        if day_of_week == "Sunday":
            result["opening_time"] = self.sunday_opening_time
            result["closing_time"] = self.sunday_closing_time
        
        if day_of_week == "Monday":
            result["opening_time"] = self.monday_opening_time
            result["closing_time"] = self.monday_closing_time
        
        if day_of_week == "Tuesday":
            result["opening_time"] = self.tuesday_opening_time
            result["closing_time"] = self.tuesday_closing_time
        
        if day_of_week == "Wednesday":
            result["opening_time"] = self.wednesday_opening_time
            result["closing_time"] = self.wednesday_closing_time
        
        if day_of_week == "Thursday":
            result["opening_time"] = self.thursday_opening_time
            result["closing_time"] = self.thursday_closing_time
        
        if day_of_week == "Friday":
            result["opening_time"] = self.friday_opening_time
            result["closing_time"] = self.friday_closing_time
        
        return result
    
    # def get_business_hour_status_from_day_of_week_and_time(self, day_of_week, time):
    #     is_open = False
    #     result = {
    #         "opening_time": None,
    #         "closing_time": None
    #     }
    #     if day_of_week == "Saturday":
    #         result["opening_time"] = self.saturday_opening_time
    #         result["closing_time"] = self.saturday_closing_time
        
    #     if day_of_week == "Sunday":
    #         result["opening_time"] = self.sunday_opening_time
    #         result["closing_time"] = self.sunday_closing_time
        
    #     if day_of_week == "Monday":
    #         result["opening_time"] = self.monday_opening_time
    #         result["closing_time"] = self.monday_closing_time
        
    #     if day_of_week == "Tuesday":
    #         result["opening_time"] = self.tuesday_opening_time
    #         result["closing_time"] = self.tuesday_closing_time
        
    #     if day_of_week == "Wednesday":
    #         result["opening_time"] = self.wednesday_opening_time
    #         result["closing_time"] = self.wednesday_closing_time
        
    #     if day_of_week == "Thursday":
    #         result["opening_time"] = self.thursday_opening_time
    #         result["closing_time"] = self.thursday_closing_time
        
    #     if day_of_week == "Friday":
    #         result["opening_time"] = self.friday_opening_time
    #         result["closing_time"] = self.friday_closing_time
        
    #     return result


"""
*** Pre-Save, Post-Save and Pre-Delete Hooks ***
"""

@receiver(post_delete, sender=StoreModerator)
def delete_users_on_store_moderator_pre_delete(sender, instance, **kwargs):
    """ Deletes Users on `StoreModerator` pre_delete hook """
    try:
        user_qs = get_user_model().objects.filter(slug=instance.user.slug)
        if user_qs:
            user_qs.delete()
    except Exception as E:
        raise Exception(f"Failed to delete `User` on `StoreModerator` post_delete hook. Exception: {str(E)}")



@receiver(post_save, sender=StoreModerator)
def update_user_fields_on_store_moderator_create(sender, instance, **kwargs):
    """ Deletes Users on `StoreModerator` post_save hook """
    try:
        instance.user.is_store_staff = True
    except Exception as E:
        raise Exception(f"Failed to update `User` on `StoreModerator` post_save hook. Exception: {str(E)}")
