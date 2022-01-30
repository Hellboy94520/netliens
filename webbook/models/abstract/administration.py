from django.db import models
from django.utils.translation import ugettext_lazy as _

from webbook.models.user import User

class Administration(models.Model):
    """
        Contains the data used by administration_only for models, not visible by Users
    """
    is_enable = models.BooleanField(
        default=False,
        verbose_name=_("Enable"),
        help_text=_("Enable to be use by Admin, Staff and User")
    )
    is_visible = models.BooleanField(
        default=False,
        verbose_name=_("Visible"),
        help_text=_("Enable to be use by Admin and Staff but not by User")
    )

    """ ------------------------- """
    creation_date = models.DateTimeField(auto_now_add=True)
    creation_user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="%(class)s_creation_user"
    )
    creation_ip = models.GenericIPAddressField(
        protocol='both',
        default=None,
        null=True,
        blank=True
    )
    last_update_date = models.DateTimeField(auto_now=True)
    approval_date = models.DateTimeField(
        default = None,
        null=True,
        blank=True
    )
    approval_user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="%(class)s_approval_user"
    )

    class Meta:
        abstract = True