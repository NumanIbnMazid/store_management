from django.db import models
from studios.models import Studio
from spaces.models import Space
from utils.snippets import simple_random_string, unique_slug_generator
from utils.image_upload_helper import upload_plan_image_path, upload_category_image_path, upload_option_image_path
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class OptionCategory(models.Model):
    number = models.IntegerField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_option_categories")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to=upload_category_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name = 'Option Category'
        verbose_name_plural = 'Option Categories'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    def clean(self):
        number_validation_qs = self.__class__.objects.filter(number=self.number)
        if self.pk:
            number_validation_qs = number_validation_qs.exclude(pk=self.pk)
        if number_validation_qs.exists():
            raise ValidationError(
                {"number": [f"{self.__class__.__name__} with this number ({self.number}) already exists!"]}
            )
        title_validation_qs = self.__class__.objects.filter(title__iexact=self.title)
        if self.pk:
            title_validation_qs = title_validation_qs.exclude(pk=self.pk)
        if title_validation_qs.exists():
            raise ValidationError(
                {"title": [f"{self.__class__.__name__} with this title ({self.title}) already exists!"]}
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(self.__class__, self).save(*args, **kwargs)
    

class Option(models.Model):
    option_category = models.ForeignKey(OptionCategory, on_delete=models.CASCADE, related_name='option_category_options')
    number = models.IntegerField()
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to=upload_option_image_path, blank=True, null=True)
    comment = models.CharField(max_length=254, blank=True, null=True)
    specification_url = models.URLField(blank=True, null=True)
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def clean(self):
        number_validation_qs = self.__class__.objects.filter(number=self.number)
        if self.pk:
            number_validation_qs = number_validation_qs.exclude(pk=self.pk)
        if number_validation_qs.exists():
            raise ValidationError(
                {"number": [f"{self.__class__.__name__} with this number ({self.number}) already exists!"]}
            )
        title_validation_qs = self.__class__.objects.filter(title__iexact=self.title)
        if self.pk:
            title_validation_qs = title_validation_qs.exclude(pk=self.pk)
        if title_validation_qs.exists():
            raise ValidationError(
                {"title": [f"{self.__class__.__name__} with this title ({self.title}) already exists!"]}
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(self.__class__, self).save(*args, **kwargs)

class Plan(models.Model):
    space = models.ManyToManyField(Space, related_name="space_plans")
    option = models.ManyToManyField(Option, blank=True, related_name='plan_options')
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_1 = models.ImageField(upload_to=upload_plan_image_path, blank=True, null=True)
    image_1_reference = models.CharField(max_length=254, blank=True, null=True)
    image_1_comment = models.CharField(max_length=254, blank=True, null=True)
    image_2 = models.ImageField(upload_to=upload_plan_image_path, blank=True, null=True)
    image_2_reference = models.CharField(max_length=254, blank=True, null=True)
    image_2_comment = models.CharField(max_length=254, blank=True, null=True)
    image_3 = models.ImageField(upload_to=upload_plan_image_path, blank=True, null=True)
    image_3_reference = models.CharField(max_length=254, blank=True, null=True)
    image_3_comment = models.CharField(max_length=254, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    explanatory_comment = models.CharField(max_length=254, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    def clean(self):
        title_validation_qs = self.__class__.objects.filter(title__iexact=self.title.lower())
        if self.pk:
            title_validation_qs = title_validation_qs.exclude(pk=self.pk)
        if title_validation_qs.exists():
            raise ValidationError(
                {"title": [f"{self.__class__.__name__} with this title ({self.title}) already exists!"]}
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(self.__class__, self).save(*args, **kwargs)


@receiver(pre_save, sender=OptionCategory)
def update_category_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates category slug on category pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.title)
        except Exception as E:
            instance.slug = simple_random_string()

@receiver(pre_save, sender=Option)
def update_option_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates option slug on option pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.title)
        except Exception as E:
            instance.slug = simple_random_string()

@receiver(pre_save, sender=Plan)
def update_product_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates product slug on product pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.title)
        except Exception as E:
            instance.slug = simple_random_string()
