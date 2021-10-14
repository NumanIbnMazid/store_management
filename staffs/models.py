from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="staff_user")
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.user.get_dynamic_username()