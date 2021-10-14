from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from utils.snippets import unique_slug_generator, simple_random_string

def autoslug(fieldname):
    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                slug = slugify(source)
                if slug:  # not all strings result in a slug value
                    instance.slug = unique_slug_generator(instance=instance, field=slug)
                else:
                    instance.slug = simple_random_string()
        return model
    return decorator