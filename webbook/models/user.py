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
from django.core.validators import MaxValueValidator, MinValueValidator

# -----------------------------
# Model
# -----------------------------
class User(AbstractUser):
    company    = models.CharField(
        max_length=100,
        default="",
        verbose_name=_("Company"),
        help_text=_("Company Name"))
    nl0 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=1,
        verbose_name=_("NL Level 0"),
        help_text=_("NL Level 0 Purchase Quantity"))
    nl1 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 1"),
        help_text=_("NL Level 1 Purchase Quantity"))
    nl2 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 2"),
        help_text=_("NL Level 2 Purchase Quantity"))
    nl3 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 3"),
        help_text=_("NL Level 3 Purchase Quantity"))
    nl4 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 4"),
        help_text=_("NL Level 4 Purchase Quantity"))
    nl5 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 5"),
        help_text=_("NL Level 5 Purchase Quantity"))
    nl6 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 6"),
        help_text=_("NL Level 6 Purchase Quantity"))
    nl7 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 7"),
        help_text=_("NL Level 7 Purchase Quantity"))

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
