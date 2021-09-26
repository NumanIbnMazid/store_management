from django.db import models
from stores.models import Store
from spaces.models import Space
from utils.snippets import simple_random_string, unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Category(models.Model):
    category_number = models.IntegerField(default=0, blank=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1, verbose_name='Studio')
    category_name = models.CharField(max_length=255, blank=False, verbose_name='Category Name')
    slug = models.SlugField(unique=True)
    category_icon = models.ImageField(default='category_icon', blank=True, verbose_name='Category Icon')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
 
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.category_name

class Time(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    def __str__(self):
        time = str(self.start) + ' - ' + str(self.end)
        return time


class Option(models.Model):
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name='category_potions')
    option_number = models.IntegerField(default=0, blank=False, unique=True)
    option_name = models.CharField(max_length=255, blank=False, verbose_name='Option Name')
    slug = models.SlugField(unique=True)
    option_icon = models.ImageField(default='option_icon', blank=True, verbose_name='Icon')
    comment = models.CharField(max_length=254, blank=True, null=True, verbose_name='Comment')
    specification_url = models.URLField(blank=True, null=True)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Price')
    daily_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.option_name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1, verbose_name='Store')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, default=1, verbose_name='Space')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, default=1, verbose_name='Option')
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name='category_products')
    reservation = models.ForeignKey(Time, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Set Time')
    product_name = models.CharField(max_length=254, blank=False, verbose_name='Product Name')
    slug = models.SlugField(unique=True)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Price')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Price')
    discount_price = models.DecimalField(max_digits=6, blank=True, null=True,default=0, decimal_places=2,verbose_name='Discount')
    image_1 = models.ImageField(upload_to='image', blank=True, verbose_name='Image One')
    image_2 = models.ImageField(upload_to='image', blank=True, verbose_name='Image Two')
    image_3 = models.ImageField(upload_to='image', blank=True, verbose_name='Image Three')
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    review = models.FloatField(default=0.0, blank=True, null=True, verbose_name='Review')
    offer = models.CharField(max_length=254, blank=True, null=True, verbose_name='Offer')
    comment = models.CharField(max_length=254, blank=True, null=True, verbose_name='Comment')
    details = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Details')
    how_to_use = models.TextField(max_length=1000, blank=True, null=True, verbose_name='How to use')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
 
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.product_name


@receiver(pre_save, sender=Category)
def update_category_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates category slug on category pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.category_name)
        except Exception as E:
            instance.slug = simple_random_string()

@receiver(pre_save, sender=Option)
def update_option_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates option slug on option pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.option_name)
        except Exception as E:
            instance.slug = simple_random_string()

@receiver(pre_save, sender=Product)
def update_product_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates product slug on product pre_save hook """
    if not instance.slug:
        try:
            instance.slug = unique_slug_generator(instance=instance, field=instance.product_name)
        except Exception as E:
            instance.slug = simple_random_string()