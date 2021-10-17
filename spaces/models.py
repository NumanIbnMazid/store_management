from django.db import models
from stores.models import Store
from utils.image_upload_helper import upload_space_image_path
from utils.helpers import model_cleaner
from utils.helpers import autoslugFromUUID


@autoslugFromUUID()
class Space(models.Model):
    name = models.CharField(max_length=150)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_spaces")
    slug = models.SlugField(unique=True)
    image_1 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_1_reference = models.CharField(max_length=254, blank=True, null=True)
    image_1_comment = models.CharField(max_length=254, blank=True, null=True)
    image_2 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_2_reference = models.CharField(max_length=254, blank=True, null=True)
    image_2_comment = models.CharField(max_length=254, blank=True, null=True)
    image_3 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_3_reference = models.CharField(max_length=254, blank=True, null=True)
    image_3_comment = models.CharField(max_length=254, blank=True, null=True)
    image_4 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_4_reference = models.CharField(max_length=254, blank=True, null=True)
    image_4_comment = models.CharField(max_length=254, blank=True, null=True)
    image_5 = models.ImageField(upload_to=upload_space_image_path, blank=True, null=True)
    image_5_reference = models.CharField(max_length=254, blank=True, null=True)
    image_5_comment = models.CharField(max_length=254, blank=True, null=True)
    equipment_details = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "Space"
        verbose_name_plural = "Spaces"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def clean(self, initialObject=None, requestObject=None):
        store_id = initialObject.store.id if initialObject else self.store.id if self.store else None
        qsFieldObjectList = [
            {
                "qs": self.__class__.objects.filter(name__iexact=self.name.lower(), store__id=store_id),
                "field": "name"
            }
        ]
        model_cleaner(selfObj=self, qsFieldObjectList=qsFieldObjectList, initialObject=initialObject)
