from django.db import models
from django.db.models.fields import PositiveIntegerField, PositiveSmallIntegerField
from utils.helpers import model_cleaner
from studios.models import Studio
from utils.helpers import autoslugFromUUID


@autoslugFromUUID()
class Coupon(models.Model):
    name = models.CharField(max_length=254)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_coupons")
    slug = models.SlugField(unique=True, max_length=254)
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
    
    def clean(self, initialObject=None, requestObject=None):
        studio_id = initialObject.studio.id if initialObject else self.studio.id if self.studio else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower(), studio__id=studio_id),
                "field": "name"
            },
            {
                "qs": self.__class__.objects.filter(code__iexact=self.code.lower(), studio__id=studio_id),
                "field": "code"
            },
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)


@autoslugFromUUID()
class PeriodicalDiscount(models.Model):
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, related_name="studio_periodical_discounts")
    slug = models.SlugField(unique=True, max_length=254)
    reservation_day_ago = models.PositiveSmallIntegerField()
    discount_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Periodical Discount'
        verbose_name_plural = 'Periodical Discounts'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name

    def clean(self, initialObject=None, requestObject=None):
        pass


@autoslugFromUUID()
class EarlyBirdDiscount(models.Model):
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, related_name="studio_earlybird_discounts")
    slug = models.SlugField(unique=True, max_length=254)
    period = models.DateTimeField()
    discount_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Early Bird Discount'
        verbose_name_plural = 'Early Bird Discounts'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name

    def clean(self, initialObject=None, requestObject=None):
        pass



@autoslugFromUUID()
class PointSetting(models.Model):
    studio = models.OneToOneField(Studio, on_delete=models.CASCADE, related_name="studio_point_setting")
    slug = models.SlugField(unique=True, max_length=254)
    point_per_yen = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Point Setting'
        verbose_name_plural = 'Point Settings'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.studio.name
    
    def clean(self, initialObject=None, requestObject=None):
        pass
