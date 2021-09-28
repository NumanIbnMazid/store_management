from django.db import models
from django.contrib.auth import get_user_model
from utils.snippets import simple_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="staff_user")
    slug = models.SlugField(unique=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.user.get_dynamic_username()


@receiver(pre_save, sender=Staff)
def update_staff_slug_on_pre_save(sender, instance, **kwargs):
    """ Generates and updates staff slug on Staff pre_save hook """
    if not instance.slug:
        instance.slug = simple_random_string()
