from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

class Customer(models.Model):
    class Identification(models.IntegerChoices):
        ALREADY = 0, _("Already")
        YET = 1, _("Yet")
        
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="customer_user")
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
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

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.user.get_dynamic_username()