from django.db import models
from studios.models import Studio
from spaces.models import Space
from utils.image_upload_helper import upload_plan_image_path, upload_category_image_path, upload_option_image_path
from utils.helpers import model_cleaner
from utils.helpers import autoslugFromUUID


@autoslugFromUUID()
class OptionCategory(models.Model):
    number = models.IntegerField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="studio_option_categories")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=254)
    icon = models.ImageField(upload_to=upload_category_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name = 'Option Category'
        verbose_name_plural = 'Option Categories'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    def clean(self, initialObject=None, requestObject=None):
        studio_id = initialObject.studio.id if initialObject else self.studio.id if self.studio else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(number=self.number, studio__id=studio_id),
                "field": "number"
            },
            {
                "qs": self.__class__.objects.filter(title__iexact=self.title, studio__id=studio_id),
                "field": "title"
            },
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)
    

@autoslugFromUUID()
class Option(models.Model):
    option_category = models.ForeignKey(OptionCategory, on_delete=models.CASCADE, related_name='option_category_options')
    number = models.IntegerField()
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=254)
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
    
    def clean(self, initialObject=None, requestObject=None):
        option_category_id = initialObject.option_category.id if initialObject else self.option_category.id if self.option_category else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(number=self.number, option_category__id=option_category_id),
                "field": "number"
            },
            {
                "qs": self.__class__.objects.filter(title__iexact=self.title, option_category__id=option_category_id),
                "field": "title"
            },
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)


@autoslugFromUUID()
class Plan(models.Model):
    space = models.ManyToManyField(Space, related_name="plan_spaces")
    option = models.ManyToManyField(Option, blank=True, related_name='plan_options')
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, max_length=254)
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
    
    def clean(self, initialObject=None, requestObject=None):
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(title__iexact=self.title.lower()),
                "field": "title"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)
