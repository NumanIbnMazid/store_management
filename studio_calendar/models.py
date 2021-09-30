from django.db import models
from studios.models import Studio
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utils.snippets import unique_slug_generator, simple_random_string

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
