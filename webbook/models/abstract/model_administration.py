from django.db import models
from django.utils.translation import ugettext_lazy as _

class ModelAdministration(models.Model):
    """
        This is a temporary model to save data from Sql Import
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

    class Meta:
        abstract = True