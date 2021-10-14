from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from utils.snippets import unique_slug_generator, simple_random_string
from utils.helpers import model_cleaner

class Studio(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="studio_user")
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    about = models.TextField(max_length=2000, blank=True, null=True)
    linkedin = models.URLField(max_length=254, blank=True, null=True)
    website = models.URLField(max_length=254, blank=True, null=True)
    facebook = models.URLField(max_length=254, blank=True, null=True)
    instagram = models.URLField(max_length=254, blank=True, null=True)
    twitter = models.URLField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    
    def clean(self):
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower()),
                "field": "name"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList)
    
class StudioModerator(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='studio_moderator_user', on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_moderators")
    slug = models.SlugField(unique=True)
    contact = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'StudioModerator'
        verbose_name_plural = 'StudioModerators'
        ordering = ["-created_at"]

    def __str__(self):
        return self.slug



class VatTax(models.Model):
    studio = models.OneToOneField(Studio, on_delete=models.CASCADE, related_name="studio_vattax")
    slug = models.SlugField(unique=True)
    vat = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    other_service = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Vat Tax'
        verbose_name_plural = 'Vat Tax'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name

class Currency(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_currency")
    country = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    currency = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currency'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name
    
    def clean(self):
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(currency__iexact=self.currency.lower()),
                "field": "currency"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList)



"""
*** Pre-Save, Post-Save and Pre-Delete Hooks ***
"""

@receiver(pre_save, sender=Studio)
def update_studio_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates studio slug on `Studio` pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.studio_currency)
        except Exception as E:
            instance.slug = simple_random_string()
            
@receiver(pre_save, sender=StudioModerator)
def update_studio_moderator_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates studio slug on `Studio` pre_save hook """
    if not instance.slug:
        instance.slug = simple_random_string()


@receiver(post_delete, sender=StudioModerator)
def delete_moderator_users_on_studio_pre_delete(sender, instance, **kwargs):
    """ Deletes Studio Moderator Users on `Studio` pre_delete hook """
    try:
        user_qs = get_user_model().objects.filter(id=instance.user.id)
        if user_qs:
            user_qs.delete()
    except Exception as E:
        raise Exception(f"Failed to delete `User` on `StudioModerator` post_delete hook. Exception: {str(E)}")


@receiver(post_delete, sender=StudioModerator)
def delete_users_on_studio_moderator_pre_delete(sender, instance, **kwargs):
    """ Deletes Users on `StudioModerator` pre_delete hook """
    try:
        user_qs = get_user_model().objects.filter(slug=instance.user.slug)
        if user_qs:
            user_qs.delete()
    except Exception as E:
        raise Exception(f"Failed to delete `User` on `StudioModerator` post_delete hook. Exception: {str(E)}")



@receiver(pre_save, sender=VatTax)
def update_vattax_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates VatTax slug using pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.studio.name) # Noman bhai can you check it why can't get studio.name 
        except Exception as E:
            instance.slug = simple_random_string()


@receiver(pre_save, sender=Currency)
def update_currency_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates Currency slug using pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.currency)
        except Exception as E:
            instance.slug = simple_random_string()
