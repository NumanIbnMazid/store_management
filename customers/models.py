from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from utils.snippets import simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Customer(models.Model):
    class Identification(models.IntegerChoices):
        ALREADY = 0, _("Already")
        YET = 1, _("Yet")
        
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="customer_user")
    slug = models.SlugField(unique=True)
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


@receiver(pre_save, sender=Customer)
def update_customer_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates customer slug on Customer pre_save hook """
    if not instance.slug:
        instance.slug = simple_random_string()
