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
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# -----------------------------
# Model
# -----------------------------
class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'last_name', 'first_name']
    objects = UserManager()

    def has_nl(self):
        if self.nl0 > 0 or self.nl1 > 0 or self.nl2 > 0 or \
            self.nl3 > 0 or self.nl4 > 0 or self.nl5 > 0 or \
            self.nl6 > 0 or self.nl7 > 0:
            return True
        return False

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
for fieldname in ['email', 'last_name', 'first_name']:
    User._meta.get_field(fieldname).blank = False
    User._meta.get_field(fieldname).null = False

# This is just for example
#TODO: Write permissions (valid_category, valid_localisation, valid_site, etc...)
#TODO: Write group(Free_user, VIP_user, Validator, Admin)
#TODO: Write accounts
