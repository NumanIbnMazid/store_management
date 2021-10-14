from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio
from django.core.exceptions import ValidationError


class Coupon(models.Model):
    name = models.CharField(max_length=254)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_coupons")
    slug = models.SlugField(unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    anytime = models.BooleanField(default=False)
    code = models.CharField(max_length=254, unique=True)
    percentage_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fixed_amount_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    
    def clean(self):
        name_validation_qs = self.__class__.objects.filter(name__iexact=self.name.lower())
        if self.pk:
            name_validation_qs = name_validation_qs.exclude(pk=self.pk)
        if name_validation_qs.exists():
            raise ValidationError(
                {"name": [f"{self.__class__.__name__} with this name ({self.name}) already exists!"]}
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(self.__class__, self).save(*args, **kwargs)

class PointSetting(models.Model):
    studio = models.OneToOneField(Studio, on_delete=models.CASCADE, related_name="studio_point_setting")
    slug = models.SlugField(unique=True)
    point_per_yen = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Point Setting'
        verbose_name_plural = 'Point Settings'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.studio.name
    
@receiver(pre_save, sender=Coupon)
def create_coupon_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates coupon slug on Coupon pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.name)
        except Exception as E:
            instance.slug = simple_random_string()
    
@receiver(pre_save, sender=PointSetting)
def create_point_setting_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates coupon slug on Point Setting pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.studio.name)
        except Exception as E:
            instance.slug = simple_random_string()
