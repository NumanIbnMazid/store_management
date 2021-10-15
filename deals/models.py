from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio
from django.core.exceptions import ValidationError
from utils.autoslug import autoslug

@autoslug("name")
class Coupon(models.Model):
    name = models.CharField(max_length=254)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_coupons")
    slug = models.SlugField(unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    anytime = models.BooleanField(default=False)
    code = models.CharField(max_length=254)
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
        errors = {}
        # name validation
        name_validation_qs = self.__class__.objects.filter(name__iexact=self.name.lower())
        if self.pk:
            name_validation_qs = name_validation_qs.exclude(pk=self.pk)
        if name_validation_qs.exists():
            errors["name"] = [f"{self.__class__.__name__} with this name ({self.name}) already exists!"]
        # code validation
        code_validation_qs = self.__class__.objects.filter(code__iexact=self.code.lower())
        if self.pk:
            code_validation_qs = code_validation_qs.exclude(pk=self.pk)
        if code_validation_qs.exists():
            errors["code"] = [f"{self.__class__.__name__} with this code ({self.code}) already exists!"]
            
        # raise exception
        if len(errors):
            raise ValidationError(
                errors
            )
@autoslug("studio")
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

