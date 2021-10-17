from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from utils.helpers import model_cleaner
from utils.helpers import autoslugFromUUID


@autoslugFromUUID()
class Studio(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="studio_user")
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    about = models.TextField(max_length=2000, blank=True, null=True)
    linkedin = models.URLField(max_length=254, blank=True, null=True)
    website = models.URLField(max_length=254, blank=True, null=True)
    facebook = models.URLField(max_length=254, blank=True, null=True)
    instagram = models.URLField(max_length=254, blank=True, null=True)
    twitter = models.URLField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def clean(self, initialObject=None, requestObject=None):
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower()),
                "field": "name"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)


@autoslugFromUUID()
class VatTax(models.Model):
    studio = models.OneToOneField(Studio, on_delete=models.CASCADE, related_name="studio_vattax")
    slug = models.SlugField(unique=True)
    vat = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    other_service = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Vat Tax'
        verbose_name_plural = 'Vat Tax'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name


@autoslugFromUUID()
class Currency(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_currency")
    country = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    currency = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currency'
        ordering = ["-created_at"]

    def __str__(self):
        return self.studio.name
    
    def clean(self, initialObject=None, requestObject=None):
        studio_id = initialObject.studio.id if initialObject else self.studio.id if self.studio else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(currency__iexact=self.currency.lower(), studio__id=studio_id),
                "field": "currency"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)