# -----------------------------
# Token
# -----------------------------
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# -----------------------------
# Model
# -----------------------------
class User(AbstractUser):
    company    = models.CharField(max_length=100,
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


# This is just for example
#TODO: Write permissions (valid_category, valid_localisation, valid_site, etc...)
#TODO: Write group(Free_user, VIP_user, Validator, Admin)
#TODO: Write accounts
