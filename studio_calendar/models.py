from django.db import models
from studios.models import Studio
from stores.models import Store
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utils.snippets import unique_slug_generator, simple_random_string
from django.utils.translation import gettext_lazy as _

class StudioCalendar(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_calendar")
    slug = models.SlugField(unique=True)
    country_code = models.CharField(default="JP", max_length=10)
    year = models.CharField(max_length=10)
    date = models.DateField()
    title = models.CharField(max_length=254, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Studio Calendar'
        verbose_name_plural = 'Studio Calendars'
        ordering = ["-created_at"]
    
    def __str__(self):
        return str(self.date)
    

class BusinessDay(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 0, _("Open")
        CLOSED = 1, _("Closed")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_business_days")
    slug = models.SlugField(unique=True)
    date = models.DateField()
    day_name = models.CharField(max_length=50)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Business Day'
        verbose_name_plural = 'Business Days'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.date)
    
    def get_status_str(self):
        if self.status == 0:
            return "Open"
        return "Closed"
    
class BusinessHour(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 0, _("Open")
        CLOSED = 1, _("Closed")
        
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="store_business_hour")
    slug = models.SlugField(unique=True)
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
        verbose_name = 'Business Hour'
        verbose_name_plural = 'Business Hours'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.date)
    

@receiver(pre_save, sender=StudioCalendar)
def update_studio_calendar_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates studio calendar slug on StudioCalendar pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(
                instance=instance, field=str(instance.date) + "__" + str(instance.studio.name[:50])
            )
        except Exception as E:
            instance.slug = simple_random_string()
    

@receiver(pre_save, sender=BusinessDay)
def create_business_day_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates business day slug on BusinessDay pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(
                instance=instance, field=str(instance.date) + "__" + str(instance.store.name[:50])
            )
        except Exception as E:
            instance.slug = simple_random_string()
    

@receiver(pre_save, sender=BusinessHour)
def create_business_hour_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates business hour slug on BusinessHour pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(
                instance=instance, field=str(instance.store.name[:50]) + "__" + "business_hour"
            )
        except Exception as E:
            instance.slug = simple_random_string()

