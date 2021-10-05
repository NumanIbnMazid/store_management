from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio


class Coupon(models.Model):
    title = models.CharField(unique=True, max_length=254)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_coupons")
    slug = models.SlugField(unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    anytime = models.BooleanField(default=False)
    code = models.CharField(max_length=254, unique=True)
    # TODO: Coupon amount reduce percentage needed
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    
@receiver(pre_save, sender=Coupon)
def create_coupon_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates coupon slug on Coupon pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.title)
        except Exception as E:
            instance.slug = simple_random_string()
