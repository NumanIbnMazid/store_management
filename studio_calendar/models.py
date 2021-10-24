from django.db import models
from studios.models import Studio
from stores.models import Store
from django.utils.translation import gettext_lazy as _
import uuid

class StudioCalendar(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_calendar")
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
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
        CLOSED = 0, _("Closed")
        OPEN = 1, _("Open")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_business_days")
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
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
            return "Closed"
        return "Open"
    
class BusinessHour(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name="store_custom_business_hour")
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
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