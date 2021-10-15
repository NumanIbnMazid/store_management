from django.db import models
from studios.models import Studio
import uuid

class Notification(models.Model):
    studio          = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_notification")
    title           = models.CharField(max_length=254, blank=True)
    slug            = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
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
 
    
