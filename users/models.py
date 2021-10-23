from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from utils.snippets import simple_random_string_with_timestamp
from utils.helpers import autoslugFromUUID


def generate_username_from_email(email):
    return email.split("@")[0][:15] + "__" + simple_random_string_with_timestamp(size=7)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


@autoslugFromUUID()
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    """ Additional Fields Starts """
    name = models.CharField(max_length=254, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=254)
    is_customer = models.BooleanField(default=False)
    is_studio_admin = models.BooleanField(default=False)
    is_store_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    """ Additional Fields Ends """
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")
        ordering = ["-date_joined"]

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.get_dynamic_username()

    def get_dynamic_username(self):
        """ Get a dynamic username for a specific user instance. if the user has a name then returns the name, if the user does not have a name but has a username then return username, otherwise returns email as username """
        if not self.name == None and not self.name == "":
            return self.name
        elif not self.username == None and not self.username == "":
            return self.username
        return self.email


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    """ Generates and updates username from user email on User pre_save hook """
    instance.username = generate_username_from_email(email=instance.email)
