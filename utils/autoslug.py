from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from utils.snippets import unique_slug_generator, simple_random_string, random_string_generator

def autoslug(fieldname):
    def decorator(model):
        # some sanity checks first
        assert hasattr(model, fieldname), f"Model has no field {fieldname!r}"
        assert hasattr(model, "slug"), "Model is missing a slug field"

        @receiver(models.signals.pre_save, sender=model, weak=False)
        def generate_slug(sender, instance, *args, raw=False, **kwargs):
            if not raw and not instance.slug:
                source = getattr(instance, fieldname)
                try:
                    slug = slugify(source)
                    Klass = instance.__class__
                    qs_exists = Klass.objects.filter(slug=slug).exists()
                    if qs_exists:
                        new_slug = "{slug}-{randstr}".format(
                            slug=slug,
                            randstr=random_string_generator(size=4)
                        )
                        instance.slug = new_slug
                    else:
                        instance.slug = slug
                except Exception as e:
                    instance.slug = simple_random_string()
        return model
    return decorator