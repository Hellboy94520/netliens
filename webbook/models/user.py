# -----------------------------
# Token
# -----------------------------
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

# -----------------------------
# Model
# -----------------------------
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'last_name', 'first_name']

    objects = CustomUserManager()

    is_vip = models.BooleanField(
        default=False,
        verbose_name=_("VIP"),
        help_text=_("Check if User is a VIP or not"))
    company = models.CharField(
        max_length=100,
        default="",
        null=True,
        blank=True,
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
    nl8 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 8"),
        help_text=_("NL Level 8 Purchase Quantity"))
    nl9 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 7"),
        help_text=_("NL Level 9 Purchase Quantity"))
    nl10 = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("NL Level 7"),
        help_text=_("NL Level 10 Purchase Quantity"))

    def __str__(self):
        return self.email

User._meta.get_field('email')._unique = True
for fieldname in ['email', 'last_name', 'first_name']:
    User._meta.get_field(fieldname).blank = False
    User._meta.get_field(fieldname).null = False

# This is just for example
#TODO: Write permissions (valid_category, valid_localisation, valid_site, etc...)
#TODO: Write group(Free_user, VIP_user, Validator, Admin)
#TODO: Write accounts
