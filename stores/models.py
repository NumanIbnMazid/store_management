from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from utils.image_upload_helper import upload_store_image_path
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class Store(models.Model):
    
    name = models.CharField(max_length=150, unique=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_stores")
    slug = models.SlugField(unique=True)
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
    

class CustomClosedDay(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_custom_closed_day")
    slug = models.SlugField(unique=True)
    date = models.DateField()
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Store Custom Closed Day'
        verbose_name_plural = 'Store Custom Closed Days'
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.date)


@receiver(pre_save, sender=Store)
def update_store_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates store slug on Store pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.name)
        except Exception as E:
            instance.slug = simple_random_string()


@receiver(pre_save, sender=CustomClosedDay)
def create_store_custom_closed_day_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates store custom closed day slug on CustomClosedDay pre_save hook """
    if not instance.slug:
        instance.slug = simple_random_string()
