from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from utils.helpers import autoslugFromUUID
import datetime
from django.db.models import Q

class CustomerQuerySet(models.query.QuerySet):

    def latest(self):
        return self.filter().order_by('-created_at')

    def search(self, reservati_start_date, reservati_end_date):
        lookups = (Q(created_at__range=[reservati_start_date, reservati_end_date]))
        return self.filter(lookups)

class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def search(self, query):
        return self.get_queryset().search(query)


@autoslugFromUUID()
class Customer(models.Model):
    class Identification(models.IntegerChoices):
        ALREADY = 0, _("Already")
        YET = 1, _("Yet")
        
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="customer_user")
    slug = models.SlugField(unique=True, max_length=254)
    furigana = models.CharField(max_length=100, blank=True, null=True)
    name_of_person_in_charge = models.PositiveIntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    prefecture = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    building_name = models.CharField(max_length=150, blank=True, null=True)
    contact_address = models.CharField(max_length=254, blank=True, null=True)
    other_contact_information = models.CharField(max_length=254, blank=True, null=True)
    identification = models.PositiveSmallIntegerField(choices=Identification.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    objects = CustomerManager()

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.user.get_dynamic_username()
        
    
    
