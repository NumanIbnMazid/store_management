from django.db import models
from stores.models import Store
from utils.image_upload_helper import upload_space_image_path
from utils.snippets import unique_slug_generator, simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Space(models.Model):
    name = models.CharField(max_length=150, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_spaces")
    slug = models.SlugField(unique=True)
    image_1 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_1_reference = models.CharField(max_length=254, blank=True, null=True)
    image_1_comment = models.CharField(max_length=254, blank=True, null=True)
    image_2 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_2_reference = models.CharField(max_length=254, blank=True, null=True)
    image_2_comment = models.CharField(max_length=254, blank=True, null=True)
    image_3 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_3_reference = models.CharField(max_length=254, blank=True, null=True)
    image_3_comment = models.CharField(max_length=254, blank=True, null=True)
    image_4 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_4_reference = models.CharField(max_length=254, blank=True, null=True)
    image_4_comment = models.CharField(max_length=254, blank=True, null=True)
    image_5 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_5_reference = models.CharField(max_length=254, blank=True, null=True)
    image_5_comment = models.CharField(max_length=254, blank=True, null=True)
    equipment_details = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "Space"
        verbose_name_plural = "Spaces"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    
    
@receiver(pre_save, sender=Space)
def update_space_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates space slug on `Space` pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.name)
        except Exception as E:
            instance.slug = simple_random_string()
