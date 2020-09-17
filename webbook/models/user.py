from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from enum import Enum
class UserType(Enum):
    User = 0,
    Staff = 1,
    Admin = 2

class User(AbstractUser):
    company    = models.CharField(max_length=100,
                                  blank=True,
                                  null=False,
                                  default="",
                                  verbose_name=_("Company"),
                                  help_text=_("Company Name"))
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('is_staff').default = False
User._meta.get_field('is_active').default = False
User._meta.get_field('is_superuser').default = False


# This is just for example
#TODO: Write permissions (valid_category, valid_localisation, valid_site, etc...)
#TODO: Write group(Free_user, VIP_user, Validator, Admin)
#TODO: Write accounts
