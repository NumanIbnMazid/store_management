from django.db import models
from utils.snippets import unique_slug_generator, simple_random_string
from utils.helpers import model_cleaner
from django.db.models.signals import pre_save
from django.dispatch import receiver
from studios.models import Studio
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
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower()),
                "field": "name"
            },
            {
                "qs": self.__class__.objects.filter(code__iexact=self.code.lower()),
                "field": "code"
            },
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList)
    

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
    
    
@receiver(pre_save, sender=PointSetting)
def create_point_setting_slug_on_pre_save(sender, instance, **kwargs):
    """ Creates coupon slug on Point Setting pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.studio.name)
        except Exception as E:
            instance.slug = simple_random_string()
