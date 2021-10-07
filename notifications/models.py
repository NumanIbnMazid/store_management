from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from utils.image_upload_helper import upload_store_image_path
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio

class Notification(models.Model):
    studio          = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_notification")
    title           = models.CharField(max_length=254, blank=True)
    slug            = models.SlugField(unique=True)
    message         = models.TextField(max_length=1000, blank=True)
    link_url        = models.URLField(blank=True, null=True)
    pdf_url         = models.URLField(blank=True, null=True)
    file            = models.FileField(blank=True, null=True)
    published_date  = models.DateField()
    published_time  = models.TimeField()
    is_published    = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at      = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title



@receiver(pre_save, sender=Notification)
def update_notification_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates store slug on Store pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.name)
        except Exception as E:
            instance.slug = simple_random_string()



 
    
